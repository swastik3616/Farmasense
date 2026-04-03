from pymongo import MongoClient
import os


def _get_mongo_client():
    """Create MongoDB client safely."""
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI is not set")

    return MongoClient(uri)


def _get_vector_store(db):
    """
    Lazy load heavy dependencies and create vector store.
    This prevents CI/test failures when dependencies are missing.
    """
    try:
        from langchain_mongodb import MongoDBAtlasVectorSearch
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as e:
        print(f"[RAG] Dependencies not installed: {e}")
        return None

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        return MongoDBAtlasVectorSearch(
            collection=db["crop_knowledge"],
            embedding=embeddings,
            index_name="default",
        )

    except Exception as e:
        print(f"[RAG] Vector store init failed: {e}")
        return None


def get_rag_context(query: str, state_or_district: str = "") -> str:
    """
    Fetch agricultural knowledge using MongoDB Atlas Vector Search.

    Returns:
        str: Combined relevant context or empty string if unavailable.
    """
    try:
        # Step 1: DB connection
        client = _get_mongo_client()
        db = client["farmsense"]

        # Step 2: Vector store (lazy-loaded)
        vector_store = _get_vector_store(db)
        if vector_store is None:
            return ""

        # Step 3: Build query
        search_query = query.strip()
        if state_or_district:
            search_query += f" in {state_or_district}"

        # Step 4: Perform similarity search
        results = vector_store.similarity_search(search_query, k=3)

        if not results:
            return ""

        # Step 5: Extract content safely
        context_chunks = []
        for doc in results:
            content = getattr(doc, "page_content", None)
            if content:
                context_chunks.append(content)

        return "\n".join(context_chunks)

    except Exception as e:
        print(f"[RAG] Failed to fetch context: {e}")
        return ""