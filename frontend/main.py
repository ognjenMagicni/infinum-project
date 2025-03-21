import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"  # Change if deployed

st.title("Chat with FastAPI")

user_input = st.text_input("Enter your message:")
if st.button("Send"):
    if user_input:
        response = requests.post(API_URL, json={"query": user_input})
        if response.status_code == 200:
            st.text(response.text)
        else:
            st.error("Error communicating with the backend.")