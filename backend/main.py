from fastapi import FastAPI
from pydantic import BaseModel
import os

from langchain.tools.tavily_search import TavilySearchResults  # Web search tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate  # Prompting
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model

def getApiKeys(file):
    return file.readline().split(" ")[1][:-1]

envFile = open("../application.env")
os.environ["OPENAI_API_KEY"] = getApiKeys(envFile)
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_API_KEY"] = getApiKeys(envFile)
os.environ["TAVILY_API_KEY"] = getApiKeys(envFile)
envFile.close()

app = FastAPI()


class RequestBody(BaseModel):
    query: str


app = FastAPI()


@app.post("/chat")
async def create_item(body: RequestBody):
    query = body.query

    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    tools = [TavilySearchResults(max_results = 2)]
    agent = create_react_agent(model, tools)

    system_template = "You are a legal advisor. You have to answer only questions about legal things. If asked something else, explain that is not your field of expertise. Do not use markdown, but you can use \n for pharagraphs"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    prompt = prompt_template.invoke({"text":query})
    response = agent.invoke(prompt)

    return response["messages"][-1].content