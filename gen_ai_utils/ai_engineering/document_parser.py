"""
Document Parsing Utilities - LlamaParse and structured data extraction

Provides utilities for parsing documents using LlamaParse, extracting structured data,
and converting documents to various formats with support for custom parsing instructions.
"""

import os
from typing import List, Optional, Dict, Any, Union, Literal
from pathlib import Path
import logging
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class ParsedDocument:
    """Represents a parsed document with metadata"""
    text: str
    source_file: str
    page_count: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "text": self.text,
            "source_file": self.source_file,
            "page_count": self.page_count,
            "metadata": self.metadata or {}
        }

    def save_markdown(self, output_path: str) -> None:
        """Save document text as markdown file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.text)
        logger.info(f"Saved markdown to {output_path}")


@dataclass
class ExtractionResult:
    """Represents structured data extraction result"""
    data: Dict[str, Any]
    source_file: str
    schema_name: Optional[str] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "data": self.data,
            "source_file": self.source_file,
            "schema_name": self.schema_name,
            "confidence": self.confidence
        }

    def save_json(self, output_path: str) -> None:
        """Save extraction result as JSON file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Saved extraction result to {output_path}")


class LlamaParseClient:
    """Client for LlamaParse document parsing service"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        result_type: Literal["markdown", "text"] = "markdown",
        parsing_instruction: Optional[str] = None,
        num_workers: int = 4,
        verbose: bool = True,
        language: str = "en",
        premium_mode: bool = False,
        use_vendor_multimodal_model: bool = False,
        vendor_multimodal_model_name: Optional[str] = None,
        invalidate_cache: bool = False,
        do_not_cache: bool = False,
        fast_mode: bool = False,
        continuous_mode: bool = False,
        page_separator: Optional[str] = None,
        page_prefix: Optional[str] = None,
        page_suffix: Optional[str] = None,
        disable_ocr: bool = False,
        bounding_box: Optional[Dict[str, float]] = None,
        target_pages: Optional[str] = None,
        gpt4o_mode: bool = False,
        gpt4o_api_key: Optional[str] = None
    ):
        """
        Initialize LlamaParseClient

        Args:
            api_key: LlamaCloud API key (or set LLAMA_CLOUD_API_KEY env var)
            result_type: Output format - "markdown" or "text"
            parsing_instruction: Custom instructions for parsing behavior
            num_workers: Number of parallel workers for processing
            verbose: Enable verbose logging
            language: Document language code (default: "en")
            premium_mode: Enable premium parsing features
            use_vendor_multimodal_model: Use vendor multimodal capabilities
            vendor_multimodal_model_name: Specific vendor model to use
            invalidate_cache: Force re-parsing cached documents
            do_not_cache: Disable caching for this request
            fast_mode: Enable faster but potentially less accurate parsing
            continuous_mode: Parse documents as continuous text
            page_separator: Custom separator between pages
            page_prefix: Prefix to add before each page
            page_suffix: Suffix to add after each page
            disable_ocr: Disable OCR processing
            bounding_box: Parse specific region (x1, y1, x2, y2)
            target_pages: Specific pages to parse (e.g., "1-5,7,9-12")
            gpt4o_mode: Enable GPT-4o multimodal parsing
            gpt4o_api_key: OpenAI API key for GPT-4o mode
        """
        try:
            from llama_parse import LlamaParse
        except ImportError:
            raise ImportError(
                "LlamaParse not installed. Install with: pip install llama-parse"
            )

        self.api_key = api_key or os.environ.get("LLAMA_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set LLAMA_CLOUD_API_KEY env var or pass api_key parameter"
            )

        # Build parser configuration
        parser_kwargs = {
            "api_key": self.api_key,
            "result_type": result_type,
            "num_workers": num_workers,
            "verbose": verbose,
            "language": language,
        }

        # Add optional parameters only if specified
        if parsing_instruction:
            parser_kwargs["parsing_instruction"] = parsing_instruction
        if premium_mode:
            parser_kwargs["premium_mode"] = premium_mode
        if use_vendor_multimodal_model:
            parser_kwargs["use_vendor_multimodal_model"] = use_vendor_multimodal_model
        if vendor_multimodal_model_name:
            parser_kwargs["vendor_multimodal_model_name"] = vendor_multimodal_model_name
        if invalidate_cache:
            parser_kwargs["invalidate_cache"] = invalidate_cache
        if do_not_cache:
            parser_kwargs["do_not_cache"] = do_not_cache
        if fast_mode:
            parser_kwargs["fast_mode"] = fast_mode
        if continuous_mode:
            parser_kwargs["continuous_mode"] = continuous_mode
        if page_separator is not None:
            parser_kwargs["page_separator"] = page_separator
        if page_prefix is not None:
            parser_kwargs["page_prefix"] = page_prefix
        if page_suffix is not None:
            parser_kwargs["page_suffix"] = page_suffix
        if disable_ocr:
            parser_kwargs["disable_ocr"] = disable_ocr
        if bounding_box:
            parser_kwargs["bounding_box"] = bounding_box
        if target_pages:
            parser_kwargs["target_pages"] = target_pages
        if gpt4o_mode:
            parser_kwargs["gpt4o_mode"] = gpt4o_mode
        if gpt4o_api_key:
            parser_kwargs["gpt4o_api_key"] = gpt4o_api_key

        self.parser = LlamaParse(**parser_kwargs)
        self.result_type = result_type
        self.verbose = verbose

    def parse_file(
        self,
        file_path: str,
        extra_info: Optional[Dict[str, Any]] = None
    ) -> List[ParsedDocument]:
        """
        Parse a single file

        Args:
            file_path: Path to file to parse
            extra_info: Additional metadata to attach

        Returns:
            List of ParsedDocument objects
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            logger.info(f"Parsing file: {file_path}")

            # Parse the document
            documents = self.parser.load_data(file_path, extra_info=extra_info)

            # Convert to ParsedDocument objects
            parsed_docs = []
            for i, doc in enumerate(documents):
                metadata = doc.metadata if hasattr(doc, 'metadata') else {}
                if extra_info:
                    metadata.update(extra_info)

                parsed_doc = ParsedDocument(
                    text=doc.text,
                    source_file=file_path,
                    page_count=len(documents),
                    metadata=metadata
                )
                parsed_docs.append(parsed_doc)

            logger.info(f"Successfully parsed {len(parsed_docs)} document(s)")
            return parsed_docs

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {str(e)}")
            raise

    def parse_files(
        self,
        file_paths: List[str],
        extra_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[ParsedDocument]]:
        """
        Parse multiple files

        Args:
            file_paths: List of file paths to parse
            extra_info: Additional metadata to attach to all files

        Returns:
            Dictionary mapping file paths to ParsedDocument lists
        """
        results = {}

        for file_path in file_paths:
            try:
                results[file_path] = self.parse_file(file_path, extra_info)
            except Exception as e:
                logger.error(f"Skipping {file_path}: {str(e)}")
                results[file_path] = []

        return results

    def parse_directory(
        self,
        directory: str,
        file_extensions: Optional[List[str]] = None,
        recursive: bool = False,
        extra_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[ParsedDocument]]:
        """
        Parse all files in a directory

        Args:
            directory: Directory path to scan
            file_extensions: List of extensions to parse (e.g., ['.pdf', '.docx'])
            recursive: Whether to scan subdirectories
            extra_info: Additional metadata to attach to all files

        Returns:
            Dictionary mapping file paths to ParsedDocument lists
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Default to common document formats
        if file_extensions is None:
            file_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.html']

        # Find files
        path = Path(directory)
        if recursive:
            files = [
                str(f) for f in path.rglob('*')
                if f.is_file() and f.suffix.lower() in file_extensions
            ]
        else:
            files = [
                str(f) for f in path.glob('*')
                if f.is_file() and f.suffix.lower() in file_extensions
            ]

        logger.info(f"Found {len(files)} files to parse in {directory}")

        return self.parse_files(files, extra_info)

    def save_parsed_documents(
        self,
        documents: List[ParsedDocument],
        output_folder: str,
        combine: bool = True,
        base_name: Optional[str] = None
    ) -> List[str]:
        """
        Save parsed documents to files

        Args:
            documents: List of parsed documents
            output_folder: Output directory
            combine: Whether to combine all documents into one file
            base_name: Base name for output files

        Returns:
            List of created file paths
        """
        os.makedirs(output_folder, exist_ok=True)
        created_files = []

        if combine:
            # Combine all documents into one file
            combined_text = "\n\n".join([doc.text for doc in documents])

            if base_name is None:
                base_name = Path(documents[0].source_file).stem if documents else "combined"

            output_path = os.path.join(output_folder, f"{base_name}.md")

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(combined_text)

            created_files.append(output_path)
            logger.info(f"Saved combined document to {output_path}")
        else:
            # Save each document separately
            for i, doc in enumerate(documents):
                if base_name is None:
                    base_name = Path(doc.source_file).stem

                output_path = os.path.join(output_folder, f"{base_name}_{i}.md")
                doc.save_markdown(output_path)
                created_files.append(output_path)

        return created_files


class LlamaExtractClient:
    """Client for structured data extraction from documents"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize LlamaExtractClient

        Args:
            api_key: LlamaCloud API key (or set LLAMA_CLOUD_API_KEY env var)
            verbose: Enable verbose logging
        """
        try:
            from llama_extract import LlamaExtract
        except ImportError:
            raise ImportError(
                "LlamaExtract not available. Install with: pip install llama-index-core llama-parse"
            )

        self.api_key = api_key or os.environ.get("LLAMA_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set LLAMA_CLOUD_API_KEY env var or pass api_key parameter"
            )

        self.extractor = LlamaExtract(api_key=self.api_key, verbose=verbose)
        self.verbose = verbose

    def extract_structured_data(
        self,
        file_path: str,
        schema: Dict[str, Any],
        schema_name: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract structured data from document using a schema

        Args:
            file_path: Path to document
            schema: JSON schema defining extraction structure
            schema_name: Name for the extraction schema

        Returns:
            ExtractionResult object
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            logger.info(f"Extracting structured data from: {file_path}")

            # Perform extraction
            result = self.extractor.extract(
                file_path=file_path,
                schema=schema
            )

            extraction = ExtractionResult(
                data=result if isinstance(result, dict) else {"result": result},
                source_file=file_path,
                schema_name=schema_name
            )

            logger.info(f"Successfully extracted data from {file_path}")
            return extraction

        except Exception as e:
            logger.error(f"Failed to extract from {file_path}: {str(e)}")
            raise

    def extract_batch(
        self,
        file_paths: List[str],
        schema: Dict[str, Any],
        schema_name: Optional[str] = None
    ) -> List[ExtractionResult]:
        """
        Extract structured data from multiple documents

        Args:
            file_paths: List of file paths
            schema: JSON schema defining extraction structure
            schema_name: Name for the extraction schema

        Returns:
            List of ExtractionResult objects
        """
        results = []

        for file_path in file_paths:
            try:
                result = self.extract_structured_data(file_path, schema, schema_name)
                results.append(result)
            except Exception as e:
                logger.error(f"Skipping {file_path}: {str(e)}")

        return results


# Convenience functions

def parse_document(
    file_path: str,
    api_key: Optional[str] = None,
    result_type: Literal["markdown", "text"] = "markdown",
    parsing_instruction: Optional[str] = None,
    output_folder: Optional[str] = None,
    combine: bool = True
) -> List[ParsedDocument]:
    """
    Quick function to parse a document

    Args:
        file_path: Path to document
        api_key: LlamaCloud API key
        result_type: Output format
        parsing_instruction: Custom parsing instructions
        output_folder: If provided, save results to this folder
        combine: Whether to combine pages into one file

    Returns:
        List of ParsedDocument objects
    """
    client = LlamaParseClient(
        api_key=api_key,
        result_type=result_type,
        parsing_instruction=parsing_instruction
    )

    documents = client.parse_file(file_path)

    if output_folder:
        client.save_parsed_documents(documents, output_folder, combine=combine)

    return documents


def extract_data(
    file_path: str,
    schema: Dict[str, Any],
    api_key: Optional[str] = None,
    output_path: Optional[str] = None
) -> ExtractionResult:
    """
    Quick function to extract structured data

    Args:
        file_path: Path to document
        schema: JSON schema for extraction
        api_key: LlamaCloud API key
        output_path: If provided, save result to this path

    Returns:
        ExtractionResult object
    """
    client = LlamaExtractClient(api_key=api_key)
    result = client.extract_structured_data(file_path, schema)

    if output_path:
        result.save_json(output_path)

    return result


def create_financial_extraction_schema() -> Dict[str, Any]:
    """Create a sample schema for extracting financial data"""
    return {
        "type": "object",
        "properties": {
            "company_name": {"type": "string"},
            "fiscal_period": {"type": "string"},
            "revenue": {"type": "number"},
            "net_income": {"type": "number"},
            "total_assets": {"type": "number"},
            "total_liabilities": {"type": "number"},
            "cash_flow": {"type": "number"},
            "key_metrics": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "metric_name": {"type": "string"},
                        "value": {"type": "number"},
                        "unit": {"type": "string"}
                    }
                }
            }
        }
    }


def create_table_extraction_schema() -> Dict[str, Any]:
    """Create a sample schema for extracting tables from documents"""
    return {
        "type": "object",
        "properties": {
            "tables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "headers": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "rows": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
