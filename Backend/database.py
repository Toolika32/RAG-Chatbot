from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")



loader = DirectoryLoader(
    "../Knowledge based",
    glob="*.txt",
    loader_cls=TextLoader
)
documents=loader.load()
print()
print("number of documents loaded",len(documents))

text_splitter=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
chunks=text_splitter.split_documents(documents)


print("Number of chunks:", len(chunks))

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Embedding model loaded successfully!")

vectorstore=FAISS.from_documents(chunks,embeddings)#Create FAISS vector database from chunks and embeddings
vectorstore.save_local("faiss_index")#save it locally

print("FAISS vector database created successfully!")

