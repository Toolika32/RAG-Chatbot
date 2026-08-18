from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# --- these two lines were missing ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print("Key loaded:", api_key is not None)
# --------------------------------------

loader = DirectoryLoader(
    "../Knowledge based",
    glob="*.txt",
    loader_cls=TextLoader
)
documents = loader.load()
print()
print("number of documents loaded", len(documents))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key          # <-- pass it explicitly, matches your other file
)
print("Embedding model loaded successfully!")

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_index")

print("FAISS vector database created successfully!")