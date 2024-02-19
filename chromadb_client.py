import os
import chromadb
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
import uuid
from langchain_community.document_loaders import PyPDFLoader
import huggingface_embedding as hf
import csv
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_file(filename):
    client = chromadb.PersistentClient(path="./db")
    collection = client.get_or_create_collection(name="project2")
    
    # Initialize text splitter and embeddings
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

    if filename.endswith('.csv'):
        def get_csv_file(filename):
            # Read the data from the CSV file
            with open(filename, "r") as f:
                # Skip the header row
                next(f)
                reader = csv.reader(f)
                return list(reader)

        data = get_csv_file(filename)


        # Flatten the data into two lists
        ids=[str(uuid.uuid1()) for arr in data]
        docs=[arr[1] for arr in data]

        # Split the data into chunks
        chunk_size = 1000

        id_chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
        doc_chunks = [docs[i:i + chunk_size] for i in range(0, len(docs), chunk_size)]
        
        for id_chunk, doc_chunk in zip(id_chunks, doc_chunks):
            collection.add(
            ids=id_chunk,
            documents=doc_chunk #,
            #metadatas=[{"city":"category"} for _ in id_chunk]
            )

    if filename.endswith('.pdf'):
        pdf_file = open(filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        documents = pdf_reader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text = text_splitter.split_documents()
        chunks = text_splitter.split_text(text)

        # Convert chunks to vector representations and store in Chroma DB
        documents_list = []
        embeddings_list = []
        ids_list = []
        
        for i, chunk in enumerate(chunks):
            vector = embeddings.embed_query(chunk)
            
            documents_list.append(chunk)
            embeddings_list.append(vector)
            ids_list.append(f"{filename}_{i}")        
        
        collection.add(
            embeddings=embeddings_list,
            documents=documents_list,
            ids=ids_list
        )

load_file("data/Jungle.pdf")



