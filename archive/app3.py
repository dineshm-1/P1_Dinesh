import streamlit as st
from llm import query_llm
import chromadb
import helpers as h


st.title("Project 2")

st.sidebar.title("Provide a context")

user_context = st.sidebar.text_area("Enter text:")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt","csv"])

context_upload_clicked = st.sidebar.button("upload conext")


if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = [
         {
             "role": "ai",
             "message": "Welcome!"
         }
        
    ]

if context_upload_clicked:
    if uploaded_file is None:
        h.loadintochroma_db(uploaded_file)

context = user_context
        
user_input = st.chat_input("Message:")

if user_input:
    prompt = f"<|system|>You're an assistant answering user's question. Answer the users question Only using the context given. Context: {context}</s><|user|>{user_input}<|assistant|>answer:"

    # prompt # rendering elements with "magic"

    st.session_state['chat-history'].append({
        "role": "user",
        "message": user_input
    })

    llm_response = query_llm(prompt)

    st.session_state['chat-history'].append({
        "role": "ai",
        "message": llm_response[0]["generated_text"]
    })

if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])