import os
from langchain_community.cache import RedisSemanticCache
from langchain_huggingface import HuggingFaceEmbeddings
import langchain

def init_semantic_cache():
    """
    Initializes Redis Semantic Caching.
    If the exact same question (semantically) is asked, it bypasses the LLM and RAG entirely.
    Very cost-effective for static crop questions.
    """
    try:
        # MiniLM is lightning fast for local embedding of short texts.
        # It maps inquiries to a dense vector space, enabling semantic match logic via Redis.
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Local redis cache instance (must match Celery broker host)
        redis_url = "redis://localhost:6379"
        
        langchain.llm_cache = RedisSemanticCache(
            embedding=embeddings,
            redis_url=redis_url,
            score_threshold=0.08  # Stricter semantic bound avoids incorrect caching
        )
        print("✅ Redis Semantic Caching initialized successfully.")
    except Exception as e:
        print(f"⚠️ Could not initialize Redis Semantic Cache: {e}")
