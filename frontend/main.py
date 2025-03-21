import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"  # Change if deployed
API_URL_CHAT = "http://127.0.0.1:8000/chat-history"

st.title("Chat with FastAPI")

st.markdown(
    """
    <style>
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
    </style>
    """,
    unsafe_allow_html=True
)

user_input = st.text_input("Enter your message:")
if st.button("Send"):
    if user_input:
        response = requests.post(API_URL, json={"query": user_input})
        if response.status_code == 200:
            st.text(response.text)
        else:
            st.error("Error communicating with the backend.")
if st.button("Chat"):
    response = requests.get(API_URL_CHAT).json()
    for r in response:
        name = r[1]
        msg = r[2]
        role_class = "user-msg" if name != "AI" else "ai-msg"
        st.markdown(f'<div class="chat-container {role_class}"><b>{name}:</b> {msg}</div>', unsafe_allow_html=True)