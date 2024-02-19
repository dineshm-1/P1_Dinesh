import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="vector_db")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#embeddings = HuggingFaceEmbeddings()
#load_dotenv()
#embeddings = HuggingFaceEmbeddings(model=os.environ['EMBEDDING_URL'], huggingfacehub_api_token=os.environ['HF_TOKEN'])

print("Embedding : "+ str(embeddings))
print ("Loading documents")

loader = DirectoryLoader('data/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)

text_loader_kwargs={'autodetect_encoding': True}
#loader = DirectoryLoader('data/', glob="**/*.txt", show_progress=True, loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)

documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

persist_directory = "db"
vectordb = Chroma.from_documents(
    documents=texts, 
    embedding=embeddings, 
    persist_directory=persist_directory,
    collection_name="vector_db"
    )
vectordb.persist()