"""
Example usage of LlamaParse and LlamaExtract utilities

This script demonstrates how to:
1. Parse documents using LlamaParse
2. Extract structured data using LlamaExtract
3. Save results to various formats
"""

import os
from dotenv import load_dotenv
from gen_ai_utils.ai_engineering import (
    LlamaParseClient,
    LlamaExtractClient,
    parse_document,
    extract_data,
    create_financial_extraction_schema,
    create_table_extraction_schema
)

# Load environment variables
load_dotenv()


def example_basic_parsing():
    """Example 1: Basic document parsing"""
    print("\n=== Example 1: Basic Document Parsing ===\n")

    # Quick function for simple parsing
    documents = parse_document(
        file_path="./data/sample.pdf",
        result_type="markdown",
        output_folder="./output/parsed"
    )

    print(f"Parsed {len(documents)} document(s)")
    for i, doc in enumerate(documents):
        print(f"\nDocument {i + 1}:")
        print(f"  Source: {doc.source_file}")
        print(f"  Text preview: {doc.text[:200]}...")


def example_advanced_parsing():
    """Example 2: Advanced parsing with custom instructions"""
    print("\n=== Example 2: Advanced Parsing with Custom Instructions ===\n")

    # Custom parsing instructions
    parsing_instruction = """
    This is a financial report containing tables, charts, and financial data.
    Please extract all numerical data accurately, preserve table structures,
    and maintain the hierarchy of section headers.
    Focus on revenue, expenses, and key financial metrics.
    """

    # Create client with advanced options
    client = LlamaParseClient(
        result_type="markdown",
        parsing_instruction=parsing_instruction,
        premium_mode=True,
        num_workers=4,
        verbose=True
    )

    # Parse the document
    documents = client.parse_file("./data/financial_report.pdf")

    # Save with custom settings
    output_files = client.save_parsed_documents(
        documents=documents,
        output_folder="./output/financial",
        combine=True,
        base_name="financial_report_parsed"
    )

    print(f"Saved {len(output_files)} file(s)")


def example_batch_parsing():
    """Example 3: Batch processing multiple documents"""
    print("\n=== Example 3: Batch Document Processing ===\n")

    client = LlamaParseClient(
        result_type="markdown",
        fast_mode=True,
        num_workers=8
    )

    # Parse all PDFs in a directory
    results = client.parse_directory(
        directory="./data/documents",
        file_extensions=['.pdf', '.docx'],
        recursive=True
    )

    print(f"Processed {len(results)} files")

    # Save each document
    for file_path, documents in results.items():
        if documents:
            print(f"\n{file_path}: {len(documents)} page(s)")
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            client.save_parsed_documents(
                documents=documents,
                output_folder="./output/batch",
                combine=True,
                base_name=base_name
            )


def example_structured_extraction_financial():
    """Example 4: Extract structured financial data"""
    print("\n=== Example 4: Structured Financial Data Extraction ===\n")

    # Use the built-in financial schema
    schema = create_financial_extraction_schema()

    # Extract data
    result = extract_data(
        file_path="./data/quarterly_report.pdf",
        schema=schema,
        output_path="./output/extracted/financial_data.json"
    )

    print(f"Extracted data from: {result.source_file}")
    print(f"Schema: {result.schema_name}")
    print(f"Data preview: {result.data}")


def example_structured_extraction_custom():
    """Example 5: Extract data with custom schema"""
    print("\n=== Example 5: Custom Schema Extraction ===\n")

    # Define custom schema for extracting product information
    product_schema = {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "price": {"type": "number"},
                        "currency": {"type": "string"},
                        "features": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "availability": {"type": "boolean"}
                    }
                }
            },
            "total_products": {"type": "integer"}
        }
    }

    # Create client and extract
    client = LlamaExtractClient()

    result = client.extract_structured_data(
        file_path="./data/product_catalog.pdf",
        schema=product_schema,
        schema_name="product_catalog"
    )

    # Save result
    result.save_json("./output/extracted/products.json")

    print(f"Extracted {len(result.data.get('products', []))} products")


def example_table_extraction():
    """Example 6: Extract tables from documents"""
    print("\n=== Example 6: Table Extraction ===\n")

    # Use the built-in table extraction schema
    schema = create_table_extraction_schema()

    client = LlamaExtractClient()

    result = client.extract_structured_data(
        file_path="./data/report_with_tables.pdf",
        schema=schema,
        schema_name="table_extraction"
    )

    print(f"Extracted {len(result.data.get('tables', []))} table(s)")

    for i, table in enumerate(result.data.get('tables', [])):
        print(f"\nTable {i + 1}: {table.get('title', 'Untitled')}")
        print(f"  Headers: {table.get('headers', [])}")
        print(f"  Rows: {len(table.get('rows', []))}")


def example_multimodal_parsing():
    """Example 7: Multimodal parsing with GPT-4o"""
    print("\n=== Example 7: Multimodal Parsing (GPT-4o) ===\n")

    # Enable GPT-4o multimodal parsing for complex documents
    client = LlamaParseClient(
        result_type="markdown",
        gpt4o_mode=True,
        gpt4o_api_key=os.environ.get("OPENAI_API_KEY"),
        parsing_instruction="""
        This document contains complex diagrams, charts, and images.
        Please describe all visual elements in detail, including:
        - Charts and their data points
        - Diagrams and their components
        - Image content and context
        - Relationships between visual and textual elements
        """
    )

    documents = client.parse_file("./data/complex_report.pdf")

    client.save_parsed_documents(
        documents=documents,
        output_folder="./output/multimodal",
        combine=True
    )

    print("Multimodal parsing completed")


def example_parse_specific_pages():
    """Example 8: Parse specific pages from a document"""
    print("\n=== Example 8: Parse Specific Pages ===\n")

    # Parse only pages 1-5 and page 10
    client = LlamaParseClient(
        result_type="markdown",
        target_pages="1-5,10"
    )

    documents = client.parse_file("./data/long_document.pdf")

    print(f"Parsed {len(documents)} page(s) from specified range")


def example_rag_pipeline():
    """Example 9: Complete RAG pipeline with document parsing"""
    print("\n=== Example 9: RAG Pipeline with Document Parsing ===\n")

    from gen_ai_utils.ai_engineering import (
        EmbeddingGenerator,
        ChromaVectorStore
    )

    # Step 1: Parse documents
    parser = LlamaParseClient(
        result_type="markdown",
        parsing_instruction="Extract all content for a Q&A knowledge base"
    )

    documents = parser.parse_file("./data/knowledge_base.pdf")

    # Step 2: Create embeddings
    embedding_gen = EmbeddingGenerator(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model="text-embedding-3-small"
    )

    # Combine document texts
    doc_texts = [doc.text for doc in documents]

    # Generate embeddings
    embeddings = embedding_gen.embed_batch(doc_texts)

    # Step 3: Store in vector database
    vector_store = ChromaVectorStore(collection_name="knowledge_base")

    for i, (text, embedding) in enumerate(zip(doc_texts, embeddings)):
        vector_store.add(
            id=f"doc_{i}",
            embedding=embedding,
            metadata={"text": text, "source": documents[i].source_file}
        )

    print(f"Indexed {len(documents)} document(s) in vector store")

    # Step 4: Query the knowledge base
    query = "What are the key features of the product?"
    query_embedding = embedding_gen.embed(query)

    results = vector_store.query(
        query_embedding=query_embedding,
        n_results=3
    )

    print(f"\nQuery: {query}")
    print(f"Found {len(results)} relevant passages")


if __name__ == "__main__":
    # Uncomment the examples you want to run

    # Basic examples
    # example_basic_parsing()
    # example_advanced_parsing()
    # example_batch_parsing()

    # Structured extraction examples
    # example_structured_extraction_financial()
    # example_structured_extraction_custom()
    # example_table_extraction()

    # Advanced examples
    # example_multimodal_parsing()
    # example_parse_specific_pages()
    # example_rag_pipeline()

    print("\n=== Examples Ready ===")
    print("Uncomment the examples you want to run in the __main__ section")
    print("\nMake sure to:")
    print("1. Set LLAMA_CLOUD_API_KEY in your .env file")
    print("2. Set OPENAI_API_KEY if using GPT-4o mode or RAG pipeline")
    print("3. Install dependencies: pip install gen-ai-utils[llamaparse]")
