import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import mlflow
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.generation.mlx_wrapper import MLXLLM

load_dotenv()

# Configuration from ENV
DB_PATH = os.getenv("CHROMA_DB_PATH", "data/chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "rag_experiments")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --- CRITICAL FIX: Detect Device ---
def get_device():
    """Detect the appropriate device for the current platform."""
    import platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "mps"
    elif system == "Linux":  # Linux (HF, Cloud)
        return "cpu"
    else:  # Windows or other
        return "cpu"

DEVICE = get_device()
print(f"🖥️ Detected Platform: {DEVICE}")
# --------------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain():
    """Builds and returns the RAG chain using LCEL."""
    
    # 1. Initialize Embeddings with detected device
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': DEVICE}  # Use detected device
    )
    
    # 2. Initialize Retriever
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 3. Initialize LLM (No arguments needed, it pulls from env)
    llm = MLXLLM()
    
    # 4. Create Prompt Template
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    custom_prompt = PromptTemplate.from_template(template)
    
    # 5. Build LCEL Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    chain = build_rag_chain()
    query = "What technologies does the RAG platform use?"
    
    print(f"\n❓ Query: {query}")
    res = chain.invoke(query)
    print("\n🤖 Answer:")
    print(res)
