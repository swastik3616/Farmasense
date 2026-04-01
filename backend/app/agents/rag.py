from pymongo import MongoClient
import os
from flask import current_app
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

def get_rag_context(query: str, state_or_district: str = "") -> str:
    """
    Fetches real agricultural knowledge from MongoDB Atlas Vector Search using an isolated synchronous client.
    """
    try:
        # Isolated sync client for Langchain synchronous nodes
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        db = client["farmsense"]
        
        # Utilizing open source HuggingFace local embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # We assume the user has a "crop_knowledge" collection with Atlas Vector Search index configured.
        collection = db["crop_knowledge"]
        
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name="default"  # Assuming standard index
        )
        
        search_query = f"{query} in {state_or_district}"
        results = vector_store.similarity_search(search_query, k=3)
        
        if not results:
            return ""
            
        return "\n".join([doc.page_content for doc in results])
        
    except Exception as e:
        print(f"[RAG] Vector Search skipped/failed: {e}")
        return ""
