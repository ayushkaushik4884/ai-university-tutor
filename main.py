from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# LangChain & Google/Pinecone Integrations
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# ---------------------------------------------------------
# 1. FastAPI Setup & CORS Middleware
# ---------------------------------------------------------
app = FastAPI(title="AI University Tutor")

# Allow Streamlit or any local client to send cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Pydantic API Schemas
# ---------------------------------------------------------
class ChatRequest(BaseModel):
    question: str
    session_id: str = "default_session"
    subject: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str

# ---------------------------------------------------------
# 3. Vector Database Connection & Retriever
# ---------------------------------------------------------
# Uses Gemini embeddings to query the vector index
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

index_name = os.environ.get("PINECONE_INDEX_NAME", "university-slides-index")
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# Retrieve top 3 relevant chunks
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ---------------------------------------------------------
# 4. Modern LCEL Pipeline (Gemini 1.5 Flash)
# ---------------------------------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)

system_prompt = (
    "You are a helpful and knowledgeable university tutor. "
    "Answer the student's question using ONLY the following context. "
    "If you don't know the answer based on the context, say so.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# LCEL: Retrieve Context -> Fill Prompt -> Call LLM -> Parse String Output
base_chain = (
    RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | format_docs
    )
    | prompt
    | llm
    | StrOutputParser()
)

# ---------------------------------------------------------
# 5. In-Memory Conversational History
# ---------------------------------------------------------
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap the chain with history management
rag_with_history = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# ---------------------------------------------------------
# 6. HTTP POST Endpoint
# ---------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response = rag_with_history.invoke(
        {"question": request.question},
        config={"configurable": {"session_id": request.session_id}}
    )
    return ChatResponse(answer=response)