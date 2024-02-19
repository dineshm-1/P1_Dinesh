from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


url = "https://storage.googleapis.com/aai-web-samples/langchain_agents_webinar.opus"
docs = AssemblyAIAudioTranscriptLoader(file_path=url).load()

print('Splitting documents')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

# modify metadata because some AssemblyAI returned metadata is not in a compatible form for the Chroma db
for text in texts:
    text.metadata = {"audio_url": text.metadata["audio_url"]}

# Make vector DB from split texts
print('Embedding texts...')
persist_directory = "db"
vectordb = Chroma.from_documents(
    documents=texts, 
    embedding=embeddings, 
    persist_directory=persist_directory,
    collection_name="vector_db"
    )
vectordb.persist()