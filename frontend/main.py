import streamlit as st
import requests
p=0
API_URL = "http://127.0.0.1:8000/chat"  # Change if deployed
API_URL_CHAT = "http://127.0.0.1:8000/chat-history"

def chat_history(row_message):
        name = row_message[1]
        msg = row_message[2]
        try:
            timestamp = row_message[4].split("T")[1][0:5]
        except:
            timestamp = "Unknown"
        role_class = "user-msg" if name != "AI" else "ai-msg"
        st.markdown(
            f"""
            <div class="chat-container {role_class}">
                <b>{name}:</b> {msg}
                <div class="timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

col1, col2 = st.columns(2)
with col1:
    st.title("Chat with FastAPI")
with col2:
    st.button("Start new session")

    
st.markdown(
    """
    <style>
        .chat-history-container {
            height: 400px;  /* Set fixed height */
            overflow-y: auto;  /* Enable scrolling */
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .chat-container {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .user-msg {
            background-color: #0078ff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
        }
        .ai-msg {
            background-color: #e5e5ea;
            color: black;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
        }
        .timestamp {
            font-size: 12px;
            color: gray;
            position: absolute;
            bottom: 5px;
            right: 10px;
        }
        .blackback{
            background-color:yellow;
        }
    </style>
    """,
    unsafe_allow_html=True
)

response = requests.get(API_URL_CHAT).json()
for r in reversed(response):
    chat_history(r) 

user_input = st.text_input("Enter your message:")
if st.button("Send"):
    p=1
    if user_input:
        response = requests.post(API_URL, json={"query": user_input})
        if response.status_code == 200:
            print(response.text)
            msg = response.text.replace("\\n","\n")
            st.markdown(response.text, unsafe_allow_html=False)
            p = 1
        else:
            st.error("Error communicating with the backend.")

    