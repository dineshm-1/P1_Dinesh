import streamlit as st
from llm import query_llm
import chromadb
import os
import huggingface_embedding as hf
import utils as h
from sentence_transformers import SentenceTransformer
import csv
import uuid
#import injest
import image as Image
from langchain import HuggingFaceHub
from langchain.chains import ConversationChain
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import HuggingFaceTextGenInference
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
#from customllm import CustomLLM
#from customllm import default_llm

load_dotenv()

client = chromadb.PersistentClient(path="./db")
collection = client.get_collection(name="vector_db")

st.title("Ask Florida Blue")

st.markdown(
        h.add_logo_str(),
        
        unsafe_allow_html=True,
    )

st.sidebar.image('florida-blue-logo_0.jpg', caption='')
# llm = default_llm()
# memory = ConversationBufferMemory(memory_key="chat_history")

if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = [
         {
             "role": "ai",
             "message": "How can I help you today?"
         }
        
    ]

# chain = ConversationalRetrievalChain.from_llm(llm, memory=memory)

user_input = st.chat_input("Message:")
 
results = collection.query(query_texts=[str(user_input)], n_results=10)
print(str(results))

top_result_text = str(results['documents'][0][0])
print(top_result_text)

if user_input:
    prompt = f"""<|system|>You're Florida Blue Chat assistant. 
    Respond more details from the context provided. Include web URL links if applicable. DO not use word context in responses.
    Respond in context with respect to Florida Blue.
    Context: {top_result_text}</s><|user|>{user_input}<|assistant|>answer:"""

    st.session_state['chat-history'].append({
            "role": "user",
            "message": user_input
        })

    llm_response = query_llm(prompt)
    #llm_response = chain({"question": prompt})

    print ("llm_response : " + str(llm_response))

    st.session_state['chat-history'].append({
            "role": "ai",
            "message": llm_response[0]["generated_text"]
        })

if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])