import os
import tempfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-assistant")

def save_uploaded_file(uploaded_file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        logger.info(f"Saved uploaded file: {uploaded_file.name}")
        return tmp.name

def cleanup_temp_file(path: str):
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Cleaned up temp file: {path}")