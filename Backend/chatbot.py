from dotenv import load_dotenv
load_dotenv()
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from retriever import retriever



api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context.

<context>
{context}
</context>

Question: {input}

If the answer is not present in the context, say:
"I don't know based on the available information."
""")

document_chain = create_stuff_documents_chain(
    llm,
    prompt
)


retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)


def get_answer(query):
    response = retrieval_chain.invoke({
        "input": query
    })

    return response["answer"]