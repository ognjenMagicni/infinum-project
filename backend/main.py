from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2
from datetime import datetime
import string
import random

from langchain.tools.tavily_search import TavilySearchResults  # Web search tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate  # Prompting
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langsmith import traceable
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Establish the connection



def getApiKeys(file):
    return file.readline().split(" ")[1][:-1]

def generate_session():
   character = string.ascii_letters
   return ''.join( random.choice(character) for _ in range(10))
   

envFile = open("../application.env")
os.environ["OPENAI_API_KEY"] = getApiKeys(envFile)
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_API_KEY"] = getApiKeys(envFile)
os.environ["TAVILY_API_KEY"] = getApiKeys(envFile)


conn = psycopg2.connect(
    host=getApiKeys(envFile),
    user=getApiKeys(envFile),
    password=getApiKeys(envFile),
    database=getApiKeys(envFile)
)
envFile.close()

folder_path = "../documents/"
loader = DirectoryLoader(folder_path, glob="*pdf", loader_cls=PyPDFLoader)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
embedding = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(embedding_function=embedding)
ids = vector_store.add_documents(all_splits)

systemInfo = """"You are a legal advisor.
 If youu feel that you can help customer about legal help answer immediately.
 If you are speaking about legal, try always to back up your story with law and article.
 You should always use tools, since they offer valid information.
 First use retriever tool, but if you think you could not get valid info, then use tavily.
 You should not answer questions about anything else except law, politely warn person about your task."""

system_template = "You are a legal advisor. You have to answer only questions about legal things. If asked something else, explain that is not your field of expertise. Do not use markdown, but you can use \n for pharagraphs. Also if possible name law you are reffering to "
prompt_template = ChatPromptTemplate.from_messages(
    [("system", systemInfo), ("user", "{messages}")]
)

def retriever(query:str):
  """
    Pronadji relevantne informacije iz pravne literature
  """
  print("Retriever je pozvan")
  retrieved_docs = vector_store.similarity_search(query,k=5)
  serialized = "\n\n".join(
      f"Source: {doc.metadata}, Content: {doc.page_content}"
      for doc in retrieved_docs
  )
  return serialized, retrieved_docs

llm = init_chat_model("gpt-4o-mini", model_provider="openai")
tavily = TavilySearchResults(max_results=1)
llm_tools = llm.bind_tools([tavily,retriever])
memory = MemorySaver()
def llm_fun(state:MessagesState):
  prompt = prompt_template.invoke({"messages":state["messages"]})
  response = llm_tools.invoke(prompt)
  return {"messages":response}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("llm",llm_fun)
graph_builder.add_edge(START,"llm")
graph_builder.add_node("tools",ToolNode([tavily,retriever]))
graph_builder.add_conditional_edges("llm",tools_condition)
graph_builder.add_edge("tools","llm")
graph_builder.add_edge("llm",END)

graph = graph_builder.compile(checkpointer=memory)

@traceable
def traceable_function(question):
  config = {"configurable":{"thread_id":"7"}}
  response = graph.invoke({"messages":question},config)
  return response

app = FastAPI()

class RequestBody(BaseModel):
    query: str


app = FastAPI()

def insert_in_database(query:str, response:str):
    cursor = conn.cursor()
    insert_query = "INSERT INTO chat_history (role, message,date) VALUES (%s, %s, %s)"
    data = [
        ("User", query, datetime.now()),
        ("AI", response, datetime.now())
    ]
    cursor.executemany(insert_query, data)
    conn.commit()

    cursor.close()

def chat_history():
    cursor = conn.cursor()
    query = "select * from chat_history WHERE date IS NOT NULL ORDER BY date DESC LIMIT 4"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def chatbot_response(query):
    response = traceable_function(query)
    return response["messages"][-1].content

@app.post("/chat")
async def create_item(body: RequestBody):
    query = body.query
    response = chatbot_response(query)
    insert_in_database(query,response)
    return response

@app.get("/chat-history")
async def get_chat_history():
    return chat_history()

@app.get("/new_session")
async def new_session():
   return generate_session()