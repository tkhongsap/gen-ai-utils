# 🚀 Gen AI Utils

**Comprehensive utilities for AI/ML Engineering, Data Science, and Data Engineering**

A professional Python toolkit providing battle-tested utilities for working with LLMs, building data pipelines, performing statistical analysis, and deploying AI applications.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🤖 AI/ML Engineering
- **OpenAI Integration**: Thread management, message processing, and analytics
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

### Basic Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### With Optional Dependencies
```bash
# All features
pip install -e ".[all]"

# Specific features
pip install -e ".[llamaparse,vectordb,streamlit]"

# Development
pip install -e ".[dev]"
```

### Using Docker
```bash
# Start all services
docker-compose up -d

# API will be available at http://localhost:8000
# Jupyter will be available at http://localhost:8888
```

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
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

#### AI Engineering
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
│   │   └── prompt_manager.py
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

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embedding APIs
- LlamaIndex for document parsing
- FastAPI for the web framework
- The Python data science community

---

## 📮 Contact

For questions or support, please open an issue on GitHub.

**Made with ❤️ for Data Scientists, AI Engineers, and Data Engineers**
