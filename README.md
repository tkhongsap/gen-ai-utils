# 🚀 Gen AI Utils

**Comprehensive utilities for AI/ML Engineering, Data Science, and Data Engineering**

A professional Python toolkit providing battle-tested utilities for working with LLMs, building data pipelines, performing statistical analysis, and deploying AI applications.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📑 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Examples](#-examples)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🤖 AI/ML Engineering
- **OpenAI Integration**: Thread management, message processing, and analytics
- **Document Parsing**: LlamaParse integration for PDF, DOCX, and other formats
- **Structured Extraction**: LlamaExtract for extracting structured data from documents
- **Embeddings**: Batch generation, caching, and similarity search
- **Vector Stores**: ChromaDB integration with similarity search
- **Model Evaluation**: Classification and regression metrics
- **Prompt Management**: Template system with versioning

### 📊 Data Science
- **Pandas Helpers**: Memory optimization, profiling, chunked reading
- **Visualization**: Quick plots, distributions, correlations, time series
- **Statistics**: Outlier detection, hypothesis testing, distribution analysis
- **Data Quality**: Missing value analysis, duplicate detection

### 🔧 Data Engineering
- **ETL Pipelines**: Extract, Transform, Load framework
- **Data Validation**: Schema validation, quality checks, relationships
- **Batch Processing**: Parallel processing with progress tracking
- **Connectors**: PostgreSQL, Redis, S3 (planned)

### 🛠️ Common Utilities
- **Configuration**: Type-safe config with Pydantic
- **Logging**: Structured JSON logging with correlation IDs
- **Caching**: Memory and file-based caching with TTL
- **Retry Logic**: Exponential backoff with jitter

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- (Optional) Docker and Docker Compose for containerized deployment

### Basic Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/gen-ai-utils.git
cd gen-ai-utils

# Install core dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

### Installation with Optional Dependencies

The package supports several optional feature sets:

| Feature | Description | Install Command |
|---------|-------------|-----------------|
| **llamaparse** | LlamaParse & LlamaExtract for document parsing | `pip install -e ".[llamaparse]"` |
| **vectordb** | ChromaDB for vector storage and similarity search | `pip install -e ".[vectordb]"` |
| **streamlit** | Streamlit for building interactive dashboards | `pip install -e ".[streamlit]"` |
| **advanced-ml** | UMAP, statsmodels for advanced ML & statistics | `pip install -e ".[advanced-ml]"` |
| **media** | YouTube transcript extraction utilities | `pip install -e ".[media]"` |
| **dev** | Development tools (pytest, black, mypy, etc.) | `pip install -e ".[dev]"` |
| **all** | All optional features combined | `pip install -e ".[all]"` |

### Example Installations
```bash
# Install with LlamaParse and Vector DB support
pip install -e ".[llamaparse,vectordb]"

# Install everything for development
pip install -e ".[all]"

# Install for data science + YouTube transcripts
pip install -e ".[advanced-ml,media]"
```

### Using Docker
```bash
# Start all services (API + dependencies)
docker-compose up -d

# API will be available at http://localhost:8000
# Jupyter will be available at http://localhost:8888 (if configured)

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file in the project root with your API keys and configuration:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.
```

#### Required Environment Variables

| Variable | Description | Required For |
|----------|-------------|--------------|
| `OPENAI_API_KEY` | Your OpenAI API key | OpenAI utilities, embeddings |
| `LLAMA_CLOUD_API_KEY` | LlamaIndex Cloud API key | LlamaParse, LlamaExtract |
| `OPENAI_MODEL` | Model to use (default: gpt-4) | OpenAI operations |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, etc.) | All utilities |

#### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_ORGANIZATION` | OpenAI organization ID | None |
| `OPENAI_TEMPERATURE` | Model temperature | 0.7 |
| `DB_HOST`, `DB_PORT`, `DB_NAME` | Database configuration | localhost, 5432, genai_utils |
| `REDIS_HOST`, `REDIS_PORT` | Redis configuration | localhost, 6379 |
| `API_HOST`, `API_PORT` | API server settings | 0.0.0.0, 8000 |

**Example `.env` file**:
```bash
# Required
OPENAI_API_KEY=sk-proj-...
LLAMA_CLOUD_API_KEY=llx-...

# Optional
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
LOG_LEVEL=INFO
DEBUG=false
```

### 2. Basic Usage

#### OpenAI Assistant
```python
from gen_ai_utils.openai import AssistantManager

# Initialize
assistant = AssistantManager(
    api_key="your-api-key",
    assistant_id="asst_..."
)

# Create conversation
thread_id = assistant.create_conversation()

# Send message
response = assistant.send_message("Hello, how can you help?")
print(response)
```

#### Data Science
```python
from gen_ai_utils.data_science import optimize_dataframe, plot_distribution
import pandas as pd

# Optimize DataFrame memory
df = pd.read_csv("large_file.csv")
df = optimize_dataframe(df)

# Quick visualization
plot_distribution(df['value'], title="Value Distribution")
```

#### Data Engineering
```python
from gen_ai_utils.data_engineering import ETLPipeline

# Create ETL pipeline
pipeline = ETLPipeline("my_pipeline")
pipeline.add_extractor(extract_from_source)
pipeline.add_transformer(clean_data)
pipeline.add_validator(validate_quality)
pipeline.add_loader(load_to_database)

# Run pipeline
result = pipeline.run()
print(f"Processed {result.records_processed} records")
```

#### AI Engineering - Embeddings
```python
from gen_ai_utils.ai_engineering import EmbeddingGenerator, semantic_search

# Generate embeddings
generator = EmbeddingGenerator(api_key="your-key")
embedding = generator.embed("Sample text")

# Semantic search
results = semantic_search(
    query="machine learning",
    documents=["AI is great", "ML helps automation", "Data science"],
    api_key="your-key",
    top_k=2
)
```

#### AI Engineering - Document Parsing
```python
from gen_ai_utils.ai_engineering import (
    parse_document,
    extract_data,
    create_financial_extraction_schema
)

# Parse a PDF document
documents = parse_document(
    file_path="./data/report.pdf",
    result_type="markdown",
    parsing_instruction="Extract all financial data and tables",
    output_folder="./output"
)

# Extract structured data
schema = create_financial_extraction_schema()
result = extract_data(
    file_path="./data/financial_report.pdf",
    schema=schema,
    output_path="./output/financial_data.json"
)

print(f"Extracted: {result.data}")
```

---

## 📂 Project Structure

```
gen-ai-utils/
├── gen_ai_utils/              # Main package
│   ├── __init__.py
│   ├── openai/                # OpenAI utilities
│   │   ├── core/
│   │   │   ├── thread_manager.py
│   │   │   ├── message_processor.py
│   │   │   └── analytics.py
│   │   └── assistants.py
│   ├── data_science/          # Data science utilities
│   │   ├── pandas_helpers.py
│   │   ├── visualization.py
│   │   └── statistics.py
│   ├── data_engineering/      # Data engineering utilities
│   │   ├── etl.py
│   │   ├── validation.py
│   │   └── batch_processor.py
│   ├── ai_engineering/        # AI/ML engineering utilities
│   │   ├── embeddings.py
│   │   ├── vector_stores.py
│   │   ├── model_evaluation.py
│   │   ├── prompt_manager.py
│   │   └── document_parser.py  # LlamaParse & LlamaExtract integration
│   ├── common/                # Common utilities
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── cache.py
│   │   └── retry.py
│   └── api/                   # FastAPI application
│       └── main.py
├── tests/                     # Test suite
│   ├── unit/
│   └── integration/
├── examples/                  # Example scripts
├── requirements.txt           # Dependencies
├── pyproject.toml            # Package configuration
├── Dockerfile                # Docker image
├── docker-compose.yml        # Docker services
└── README.md                 # This file
```

---

## 📚 Documentation

### OpenAI Utilities

#### Thread Manager
```python
from gen_ai_utils.openai.core import ThreadManager

manager = ThreadManager(api_key="your-key")

# Create thread
thread_id = manager.create_thread()

# Add message
manager.add_message(thread_id, "Hello!")

# Get messages
messages = manager.get_messages(thread_id)
```

#### Message Analytics
```python
from gen_ai_utils.openai.core import MessageAnalytics

analytics = MessageAnalytics()

# Categorize messages
categorized = analytics.categorize_messages(messages)

# Get sentiment distribution
sentiments = analytics.get_sentiment_distribution(messages)

# Generate report
report = analytics.generate_report(messages)
print(report)
```

### Data Science Utilities

#### Pandas Helpers
```python
from gen_ai_utils.data_science import (
    optimize_dataframe,
    profile_dataframe,
    missing_values_report
)

# Memory optimization
df_optimized = optimize_dataframe(df)

# Profiling
profile = profile_dataframe(df)
print(f"Memory: {profile['memory_usage_mb']:.2f} MB")

# Missing values
report = missing_values_report(df)
```

#### Visualization
```python
from gen_ai_utils.data_science import (
    plot_distribution,
    plot_correlation_matrix,
    plot_time_series
)

# Distribution plot
plot_distribution(df['sales'], bins=50)

# Correlation heatmap
plot_correlation_matrix(df, method='pearson')

# Time series
plot_time_series(df, 'date', ['revenue', 'profit'])
```

#### Statistics
```python
from gen_ai_utils.data_science import (
    detect_outliers,
    test_normality,
    statistical_tests
)

# Detect outliers
outliers = detect_outliers(df['value'], method='iqr')
print(f"Found {outliers.sum()} outliers")

# Test normality
normality = test_normality(df['value'])
print(f"Is normal: {normality['shapiro_wilk']['is_normal']}")

# Statistical tests
results = statistical_tests(group1, group2, test_type='auto')
print(f"Significant: {results['significant']}")
```

### Data Engineering Utilities

#### ETL Pipeline
```python
from gen_ai_utils.data_engineering import ETLPipeline

pipeline = ETLPipeline("data_pipeline")

# Define stages
def extract_data():
    return pd.read_csv("source.csv")

def transform_data(df):
    return df.dropna()

def validate_data(df):
    return len(df) > 0, []

def load_data(df):
    df.to_csv("output.csv", index=False)

# Build pipeline
pipeline.add_extractor(extract_data)
pipeline.add_transformer(transform_data)
pipeline.add_validator(validate_data)
pipeline.add_loader(load_data)

# Execute
result = pipeline.run()
```

#### Data Validation
```python
from gen_ai_utils.data_engineering import (
    validate_schema,
    validate_range,
    validate_not_null
)

# Schema validation
schema = {'id': int, 'name': str, 'value': float}
is_valid, errors = validate_schema(df, schema)

# Range validation
is_valid, errors = validate_range(df, 'age', min_value=0, max_value=120)

# Not null validation
is_valid, errors = validate_not_null(df, ['required_col'])
```

#### Batch Processing
```python
from gen_ai_utils.data_engineering import BatchProcessor, parallel_process

# Batch processor
processor = BatchProcessor(batch_size=1000, max_workers=4)
result_df = processor.process_dataframe(df, transform_function)

# Simple parallel processing
results = parallel_process(items, process_func, max_workers=10)
```

### AI Engineering Utilities

#### Embeddings
```python
from gen_ai_utils.ai_engineering import EmbeddingGenerator

generator = EmbeddingGenerator(api_key="your-key")

# Single embedding
emb = generator.embed("Text to embed")

# Batch embeddings
embs = generator.embed_batch(texts, batch_size=100)

# Similarity
from gen_ai_utils.ai_engineering import cosine_similarity
sim = cosine_similarity(emb1, emb2)
```

#### Vector Stores
```python
from gen_ai_utils.ai_engineering import ChromaVectorStore

store = ChromaVectorStore(collection_name="my_docs")

# Add embeddings
store.add(embeddings, metadata=[{"doc_id": i} for i in range(len(embeddings))])

# Search
results = store.search(query_embedding, top_k=5)
```

#### Model Evaluation
```python
from gen_ai_utils.ai_engineering import evaluate_classification, evaluate_regression

# Classification metrics
metrics = evaluate_classification(y_true, y_pred, labels=['A', 'B', 'C'])
print(f"Accuracy: {metrics['accuracy']:.3f}")

# Regression metrics
metrics = evaluate_regression(y_true, y_pred)
print(f"RMSE: {metrics['rmse']:.3f}")
```

#### Prompt Management
```python
from gen_ai_utils.ai_engineering import PromptManager

manager = PromptManager()

# Add prompt template
manager.add("greeting", "Hello {name}, welcome to {place}!")

# Format prompt
prompt = manager.format("greeting", name="Alice", place="Wonderland")

# Save/load prompts
manager.save("prompts.json")
manager.load("prompts.json")
```

---

## 📚 Examples

The `examples/` directory contains practical examples demonstrating various utilities:

### Available Examples

#### 1. Document Parsing (`document_parsing_example.py`)
Demonstrates how to use LlamaParse and LlamaExtract for:
- Parsing PDF and DOCX documents
- Extracting structured data (financial reports, invoices, etc.)
- Customizing extraction schemas
- Batch document processing

```bash
# Run the document parsing example
python examples/document_parsing_example.py
```

#### 2. YouTube Transcript Extraction (`00-extract-youtube-transcript.py`)
Shows how to extract and process YouTube video transcripts:
- Fetch transcripts from YouTube videos
- Process and clean transcript text
- Save transcripts for analysis

```bash
# Extract YouTube transcript
python examples/00-extract-youtube-transcript.py
```

#### 3. ArXiv Article Extraction (`00-extract-arxiv-articles.py`)
Demonstrates extracting and processing research papers:
- Search and download ArXiv papers
- Extract text and metadata
- Process academic content

```bash
# Extract ArXiv articles
python examples/00-extract-arxiv-articles.py
```

### Running Examples

1. **Set up environment variables** (see `.env.example`):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install required dependencies**:
   ```bash
   pip install -e ".[all]"  # Or specific features needed
   ```

3. **Run the example**:
   ```bash
   python examples/<example_name>.py
   ```

---

## 🌐 API Documentation

### FastAPI Server

The package includes a FastAPI-based REST API for accessing utilities remotely.

#### Starting the API Server

```bash
# Using uvicorn directly
uvicorn gen_ai_utils.api.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
docker-compose up -d
```

#### API Endpoints

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

#### Example API Calls

```bash
# Health check
curl http://localhost:8000/health

# Parse document (example endpoint)
curl -X POST http://localhost:8000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/document.pdf"}'
```

#### Configuration

Configure the API server using environment variables in `.env`:

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
OPENAI_API_KEY=your_key_here
LLAMA_CLOUD_API_KEY=your_llamaparse_key_here
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gen_ai_utils --cov-report=html

# Run specific test file
pytest tests/unit/test_pandas_helpers.py

# Run with markers
pytest -m unit        # Only unit tests
pytest -m integration # Only integration tests
```

---

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
# Build image
docker build -t gen-ai-utils:latest .

# Run container
docker run -p 8000:8000 --env-file .env gen-ai-utils:latest
```

---

## 🔧 Troubleshooting

### Common Issues

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'gen_ai_utils'`

**Solution**:
```bash
# Make sure you've installed the package in editable mode
pip install -e .

# Or reinstall
pip uninstall gen-ai-utils
pip install -e .
```

#### API Key Issues

**Problem**: `AuthenticationError` or `Invalid API key`

**Solution**:
1. Check that you've copied `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your actual API keys to `.env`:
   ```bash
   OPENAI_API_KEY=sk-your-actual-key-here
   LLAMA_CLOUD_API_KEY=llx-your-actual-key-here
   ```
3. Ensure environment variables are loaded:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

#### LlamaParse/LlamaExtract Errors

**Problem**: `ImportError: llama_parse not found`

**Solution**:
```bash
# Install LlamaParse dependencies
pip install -e ".[llamaparse]"
```

#### ChromaDB/Vector Store Issues

**Problem**: `ImportError: chromadb not found` or `PersistentClient` errors

**Solution**:
```bash
# Install vector database dependencies
pip install -e ".[vectordb]"

# If using persistent storage, ensure directory exists
mkdir -p ./chroma_data
```

#### Memory Issues with Large DataFrames

**Problem**: `MemoryError` when processing large datasets

**Solution**:
```python
from gen_ai_utils.data_science import optimize_dataframe

# Optimize DataFrame memory usage
df = optimize_dataframe(df, aggressive=True)

# Or read in chunks
for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    process_chunk(chunk)
```

#### Docker Issues

**Problem**: Docker containers fail to start

**Solution**:
```bash
# Check Docker is running
docker --version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f
```

#### Testing Failures

**Problem**: Tests fail with import errors

**Solution**:
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Ensure you're in the correct directory
cd /path/to/gen-ai-utils
pytest
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Most utilities use structured logging
2. **Enable debug mode**: Set `DEBUG=true` in `.env`
3. **Review examples**: Check the `examples/` directory for working code
4. **Open an issue**: Report bugs on GitHub with:
   - Error message and stack trace
   - Python version (`python --version`)
   - Package versions (`pip freeze`)
   - Steps to reproduce

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/gen-ai-utils.git
   cd gen-ai-utils
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

### Code Quality Standards

- **Formatting**: Use `black` for code formatting
  ```bash
  black gen_ai_utils/ tests/
  ```

- **Linting**: Run `flake8` to check code quality
  ```bash
  flake8 gen_ai_utils/ tests/
  ```

- **Type Checking**: Use `mypy` for type hints
  ```bash
  mypy gen_ai_utils/
  ```

- **Testing**: Write tests for new features
  ```bash
  pytest tests/ --cov=gen_ai_utils
  ```

### Contribution Workflow

1. Make your changes
2. Add tests for new functionality
3. Ensure all tests pass
4. Format code with black
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include tests for new features
- Update documentation as needed
- Ensure CI passes

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

This project builds upon amazing open-source tools and services:

- **[OpenAI](https://openai.com/)** - GPT models, embeddings, and assistants API
- **[LlamaIndex](https://www.llamaindex.ai/)** - LlamaParse and LlamaExtract for document intelligence
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for building APIs
- **[Pydantic](https://pydantic.dev/)** - Data validation and settings management
- **[Pandas](https://pandas.pydata.org/)** - Powerful data analysis toolkit
- **[Scikit-learn](https://scikit-learn.org/)** - Machine learning library
- **[ChromaDB](https://www.trychroma.com/)** - AI-native embedding database
- **[Streamlit](https://streamlit.io/)** - Fast way to build data apps

Special thanks to the broader Python data science and AI community for their continuous innovation and support.

---

## 📮 Contact & Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/yourusername/gen-ai-utils/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/yourusername/gen-ai-utils/discussions)
- **Documentation**: Read the full docs at the [project homepage](https://github.com/yourusername/gen-ai-utils)

---

## 📊 Project Stats

- **Version**: 1.0.0
- **Python Support**: 3.9, 3.10, 3.11, 3.12
- **License**: MIT
- **Status**: Beta (actively maintained)

---

## 🚀 What's Next?

Planned features and improvements:

- [ ] Additional database connectors (MySQL, MongoDB, Snowflake)
- [ ] Advanced caching strategies (Redis integration)
- [ ] More ML model evaluation metrics
- [ ] Streaming API support for large files
- [ ] Integration with more LLM providers (Anthropic Claude, Google PaLM)
- [ ] Enhanced monitoring and observability tools
- [ ] Jupyter notebook examples
- [ ] Video tutorials and documentation

---

**Made with ❤️ for Data Scientists, AI Engineers, and Data Engineers**

*Star ⭐ this repository if you find it useful!*
