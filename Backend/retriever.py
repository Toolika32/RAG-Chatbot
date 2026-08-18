from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",google_api_key=os.getenv("GOOGLE_API_KEY")

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS database loaded successfully!")

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

print("Retriever created successfully!")
