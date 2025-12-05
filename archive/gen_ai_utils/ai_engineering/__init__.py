"""
AI Engineering Utilities - Embeddings, vector stores, model evaluation, and document parsing
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
from gen_ai_utils.ai_engineering.document_parser import (
    LlamaParseClient,
    LlamaExtractClient,
    ParsedDocument,
    ExtractionResult,
    parse_document,
    extract_data,
    create_financial_extraction_schema,
    create_table_extraction_schema
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
    # Document parsing and extraction
    "LlamaParseClient",
    "LlamaExtractClient",
    "ParsedDocument",
    "ExtractionResult",
    "parse_document",
    "extract_data",
    "create_financial_extraction_schema",
    "create_table_extraction_schema",
]
