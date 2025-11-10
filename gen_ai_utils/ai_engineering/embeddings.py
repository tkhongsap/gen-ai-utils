"""
Embedding Utilities - Text embeddings generation and similarity search

Provides utilities for generating embeddings using OpenAI, caching,
batch processing, and similarity calculations.
"""

import numpy as np
from typing import List, Optional, Dict, Any, Union
from openai import OpenAI
import logging
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate and manage text embeddings"""

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        cache_enabled: bool = True
    ):
        """
        Initialize EmbeddingGenerator

        Args:
            api_key: OpenAI API key
            model: Embedding model to use
            cache_enabled: Whether to cache embeddings
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, List[float]] = {}

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(f"{self.model}:{text}".encode()).hexdigest()

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        if self.cache_enabled:
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                return self._cache[cache_key]

        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding

            if self.cache_enabled:
                self._cache[cache_key] = embedding

            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 100,
        show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch
            show_progress: Whether to show progress

        Returns:
            List of embedding vectors
        """
        embeddings = []

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            if show_progress:
                print(f"Processing batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")

            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )

                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)

                # Cache results
                if self.cache_enabled:
                    for text, embedding in zip(batch, batch_embeddings):
                        cache_key = self._get_cache_key(text)
                        self._cache[cache_key] = embedding

            except Exception as e:
                logger.error(f"Batch embedding failed: {str(e)}")
                raise

        return embeddings

    def clear_cache(self):
        """Clear embedding cache"""
        self._cache.clear()

    def cache_size(self) -> int:
        """Get number of cached embeddings"""
        return len(self._cache)


def batch_embed(
    texts: List[str],
    api_key: str,
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> List[List[float]]:
    """
    Simple function to batch embed texts

    Args:
        texts: List of texts
        api_key: OpenAI API key
        model: Embedding model
        batch_size: Batch size

    Returns:
        List of embeddings
    """
    generator = EmbeddingGenerator(api_key=api_key, model=model)
    return generator.embed_batch(texts, batch_size=batch_size)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0 to 1)
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)

    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate Euclidean distance between two vectors

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Euclidean distance
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    return float(np.linalg.norm(vec1_np - vec2_np))


def find_most_similar(
    query_embedding: List[float],
    embeddings: List[List[float]],
    top_k: int = 5
) -> List[tuple]:
    """
    Find most similar embeddings to query

    Args:
        query_embedding: Query embedding vector
        embeddings: List of candidate embeddings
        top_k: Number of results to return

    Returns:
        List of (index, similarity_score) tuples
    """
    similarities = [
        (i, cosine_similarity(query_embedding, emb))
        for i, emb in enumerate(embeddings)
    ]

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


def cluster_embeddings(
    embeddings: List[List[float]],
    n_clusters: int = 5,
    method: str = 'kmeans'
) -> List[int]:
    """
    Cluster embeddings using specified method

    Args:
        embeddings: List of embedding vectors
        n_clusters: Number of clusters
        method: Clustering method ('kmeans', 'dbscan', 'hierarchical')

    Returns:
        List of cluster labels
    """
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

    X = np.array(embeddings)

    if method == 'kmeans':
        clusterer = KMeans(n_clusters=n_clusters, random_state=42)
    elif method == 'dbscan':
        clusterer = DBSCAN(eps=0.5, min_samples=5)
    elif method == 'hierarchical':
        clusterer = AgglomerativeClustering(n_clusters=n_clusters)
    else:
        raise ValueError(f"Unknown clustering method: {method}")

    labels = clusterer.fit_predict(X)
    return labels.tolist()


def reduce_dimensions(
    embeddings: List[List[float]],
    n_components: int = 2,
    method: str = 'pca'
) -> np.ndarray:
    """
    Reduce embedding dimensions for visualization

    Args:
        embeddings: List of embedding vectors
        n_components: Target number of dimensions
        method: Reduction method ('pca', 'tsne', 'umap')

    Returns:
        Reduced embeddings as numpy array
    """
    X = np.array(embeddings)

    if method == 'pca':
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=n_components)
    elif method == 'tsne':
        from sklearn.manifold import TSNE
        reducer = TSNE(n_components=n_components, random_state=42)
    elif method == 'umap':
        try:
            import umap
            reducer = umap.UMAP(n_components=n_components, random_state=42)
        except ImportError:
            raise ImportError("UMAP requires 'umap-learn' package: pip install umap-learn")
    else:
        raise ValueError(f"Unknown reduction method: {method}")

    reduced = reducer.fit_transform(X)
    return reduced


def semantic_search(
    query: str,
    documents: List[str],
    api_key: str,
    top_k: int = 5,
    model: str = "text-embedding-3-small"
) -> List[tuple]:
    """
    Perform semantic search over documents

    Args:
        query: Search query
        documents: List of documents to search
        api_key: OpenAI API key
        top_k: Number of results
        model: Embedding model

    Returns:
        List of (doc_index, similarity_score, document) tuples
    """
    generator = EmbeddingGenerator(api_key=api_key, model=model)

    # Embed query
    query_embedding = generator.embed(query)

    # Embed documents
    doc_embeddings = generator.embed_batch(documents)

    # Find most similar
    results = find_most_similar(query_embedding, doc_embeddings, top_k=top_k)

    # Return with documents
    return [(idx, score, documents[idx]) for idx, score in results]


def average_embeddings(embeddings: List[List[float]]) -> List[float]:
    """
    Calculate average of multiple embeddings

    Args:
        embeddings: List of embedding vectors

    Returns:
        Average embedding vector
    """
    return np.mean(embeddings, axis=0).tolist()
