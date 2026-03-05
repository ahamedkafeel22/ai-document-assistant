import streamlit as st
import os
from dotenv import load_dotenv
from app.document_processor import load_and_split_pdf
from app.embeddings import create_vector_store
from app.rag_chain import create_rag_chain, ask_question
from app.utils import save_uploaded_file, cleanup_temp_file

load_dotenv()

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Assistant")
st.markdown("**Upload a PDF and ask questions — powered by GPT-4o + RAG**")

# Session state
if "chain" not in st.session_state:
    st.session_state.chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

# Sidebar
with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and not st.session_state.document_loaded:
        with st.spinner("Processing document..."):
            tmp_path = save_uploaded_file(uploaded_file)
            chunks = load_and_split_pdf(tmp_path)
            vector_store = create_vector_store(chunks)
            st.session_state.chain = create_rag_chain(vector_store)
            st.session_state.document_loaded = True
            cleanup_temp_file(tmp_path)
        st.success(f"✅ Document loaded! {len(chunks)} chunks created.")

    if st.session_state.document_loaded:
        st.info("Document is ready. Ask your questions!")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.session_state.chain = None
        st.session_state.document_loaded = False
        st.rerun()

# Chat interface
if st.session_state.document_loaded:
    st.markdown("---")
    st.subheader("💬 Ask a Question")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input
    question = st.chat_input("Ask anything about your document...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask_question(st.session_state.chain, question)
                answer = result["answer"]
                st.write(answer)

                # Show sources
                with st.expander("📚 Source Pages"):
                    for src in result["sources"]:
                        st.write(f"Page {src.get('page', 'N/A')} — {src.get('source', 'document')}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })
else:
    st.info("👈 Upload a PDF document from the sidebar to get started.")
    st.markdown("""
    ### How it works:
    1. **Upload** any PDF document
    2. **Ask** questions in natural language
    3. **Get** answers powered by GPT-4o with source citations

    ### Example questions:
    - *"What is the main topic of this document?"*
    - *"Summarize the key findings"*
    - *"What does the document say about X?"*
    """)