"""
AI Engineering Utilities - Embeddings, vector stores, and model evaluation
"""

from gen_ai_utils.ai_engineering.embeddings import (
    EmbeddingGenerator,
    batch_embed,
    cosine_similarity
)
from gen_ai_utils.ai_engineering.vector_stores import (
    VectorStore,
    ChromaVectorStore,
    search_similar
)
from gen_ai_utils.ai_engineering.model_evaluation import (
    evaluate_classification,
    evaluate_regression,
    calculate_metrics
)
from gen_ai_utils.ai_engineering.prompt_manager import (
    PromptTemplate,
    PromptManager,
    load_prompts
)

__all__ = [
    # Embeddings
    "EmbeddingGenerator",
    "batch_embed",
    "cosine_similarity",
    # Vector stores
    "VectorStore",
    "ChromaVectorStore",
    "search_similar",
    # Model evaluation
    "evaluate_classification",
    "evaluate_regression",
    "calculate_metrics",
    # Prompt management
    "PromptTemplate",
    "PromptManager",
    "load_prompts",
]
