import streamlit as st
from llm import query_llm
import chromadb
import os
import huggingface_embedding as hf
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
#from   import LangChainInterface

#client = chromadb.PersistentClient(path="./db")
#collection = client.get_or_create_collection(name="project2")

st.cache_resource

def load_pdf(pdf_file):
    loaders = [PyPDFLoader(pdf_file)]

    index = VectorstoreIndexCreator(
        embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L2-v2'),
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap=0)
    ).from_loaders(loaders)
    return index

index = load_pdf('ContactFB.pdf')

hugging_face = hf.HuggingFaceEmbeddingInference(os.environ['api_url'],os.environ['api_key'])
    
chain = RetrievalQA.from_chain_type(
    llm=hugging_face,
    chain_type='stuff',
    retreiver = index.Vectorstore
)


st.title("Ask Me")
st.sidebar.title("Provide a context")

user_context = st.sidebar.text_area("Enter text:")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt","csv"])

if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = [
         {
             "role": "ai",
             "message": "How can I help you today?"
         }
        
    ]

user_input = st.chat_input("Message:")

if user_input:
    prompt = f"<|system|>You're an assistant answering user's question. Answer the users question Only using the context given. Context: {context}</s><|user|>{user_input}<|assistant|>answer:"

    # prompt # rendering elements with "magic"

    st.session_state['chat-history'].append({
        "role": "user",
        "message": user_input
    })

    llm_response = query_llm(prompt)
    #llm_response = hugging_face(prompt)

    st.session_state['chat-history'].append({
        "role": "ai",
        "message": llm_response[0]["generated_text"]
    })

if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])