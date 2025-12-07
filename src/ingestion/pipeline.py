# src/ingestion/pipeline.py
import os
import mlflow
import chromadb
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATA_PATH = "data/raw"
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "rag_experiments"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class IngestionPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'mps'}  # Use M4 MPS for embeddings
        )
        
    def load_documents(self):
        """Loads text files from the data directory."""
        loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
        documents = loader.load()
        print(f"📄 Loaded {len(documents)} documents.")
        return documents

    def chunk_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """Splits documents into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        print(f"🧩 Split into {len(chunks)} chunks.")
        return chunks

    def store_embeddings(self, chunks):
        """Embeds chunks and stores them in ChromaDB."""
        if os.path.exists(DB_PATH):
            print("⚠️ Existing DB found. Appending...")
            
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=DB_PATH,
            collection_name=COLLECTION_NAME
        )
        print(f"💾 Saved to {DB_PATH}")
        return vectorstore

    def run(self):
        """Runs the full pipeline with MLflow tracking."""
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        
        with mlflow.start_run(run_name="Ingestion_Phase_2"):
            # Log Parameters
            mlflow.log_param("embedding_model", EMBEDDING_MODEL)
            mlflow.log_param("chunk_size", 1000)
            mlflow.log_param("chunk_overlap", 200)
            
            # Execute Steps
            docs = self.load_documents()
            chunks = self.chunk_documents(docs)
            self.store_embeddings(chunks)
            
            # Log Metrics
            mlflow.log_metric("num_documents", len(docs))
            mlflow.log_metric("num_chunks", len(chunks))
            
            print("✅ Ingestion complete and logged to Dagshub!")

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
