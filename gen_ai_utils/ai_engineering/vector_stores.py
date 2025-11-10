"""Vector Store implementations for similarity search"""

from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np


class VectorStore(ABC):
    """Abstract base class for vector stores"""

    @abstractmethod
    def add(self, embeddings: List[List[float]], metadata: Optional[List[Dict]] = None):
        """Add embeddings to store"""
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        """Search for similar embeddings"""
        pass

    @abstractmethod
    def delete(self, ids: List[int]):
        """Delete embeddings by ID"""
        pass


class ChromaVectorStore(VectorStore):
    """ChromaDB vector store implementation"""

    def __init__(self, collection_name: str = "default", persist_directory: Optional[str] = None):
        try:
            import chromadb
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(name=collection_name)
        except ImportError:
            raise ImportError("ChromaDB not installed: pip install chromadb")

    def add(self, embeddings: List[List[float]], metadata: Optional[List[Dict]] = None):
        ids = [str(i) for i in range(len(embeddings))]
        self.collection.add(embeddings=embeddings, ids=ids, metadatas=metadata)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return [(int(id), dist) for id, dist in zip(results['ids'][0], results['distances'][0])]

    def delete(self, ids: List[int]):
        self.collection.delete(ids=[str(i) for i in ids])


def search_similar(embeddings: List[List[float]], query: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
    """Simple similarity search without vector DB"""
    from gen_ai_utils.ai_engineering.embeddings import cosine_similarity
    similarities = [(i, cosine_similarity(query, emb)) for i, emb in enumerate(embeddings)]
    return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
