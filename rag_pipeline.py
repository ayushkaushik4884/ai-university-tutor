import os
from typing import Optional

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_pinecone import PineconeVectorStore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set")


INDEX_NAME = "ai-university-tutor"


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


vector_store = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.3
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful university tutor.

Answer the question using ONLY the context provided below.

If the answer is not present in the context, say that the information
is not available in the provided study material.

Keep the explanation clear and easy to understand.

Context:
{context}
"""
    ),
    (
        "human",
        "{question}"
    )
])


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


rag_chain = (
    RunnablePassthrough.assign(
        context=retriever | format_docs
    )
    | prompt
    | llm
    | StrOutputParser()
)


def ask_tutor(question: str, subject: Optional[str] = None):

    if subject:
        retriever.search_kwargs = {
            "k": 3,
            "filter": {
                "Subject": subject
            }
        }
    else:
        retriever.search_kwargs = {
            "k": 3
        }

    return rag_chain.invoke({
        "question": question
    })


if __name__ == "__main__":
    question = input("Ask a question: ")

    answer = ask_tutor(question)

    print("\nAnswer:")
    print(answer)