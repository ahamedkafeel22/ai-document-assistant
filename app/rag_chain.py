from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def create_rag_chain(vector_store):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Answer questions based on the provided context.
If you cannot find the answer in the context, say so clearly.

Context: {context}"""),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough(),
            "chat_history": lambda x: []
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return {"chain": chain, "retriever": retriever}

def ask_question(chain_dict, question: str):
    chain = chain_dict["chain"]
    retriever = chain_dict["retriever"]

    docs = retriever.invoke(question)
    answer = chain.invoke(question)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }