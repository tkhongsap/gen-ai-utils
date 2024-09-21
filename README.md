
# 🚀 AI-Powered Code Assistant

This project is an AI-powered code assistant that leverages cutting-edge natural language processing and retrieval-augmented generation (RAG) techniques. The assistant provides intelligent code assistance, document parsing, and interaction with OpenAI's powerful language models, such as GPT-4, to deliver accurate and context-aware code suggestions and analysis.

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Common Utilities](#common-utilities)
- [FastAPI Module](#fastapi-module)
- [LlamaParse Utilities](#llamaparse-utilities)
- [OpenAI Utilities](#openai-utilities)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

- ⚡ **FastAPI Backend**: A robust and lightweight API framework that handles code-related queries and integrates easily with the AI models.
- 📄 **LlamaParse Integration**: Advanced document parsing using LlamaParse for structured information extraction from complex documents (e.g., financial reports, PDFs).
- 🤖 **OpenAI GPT-4 Integration**: Seamless integration with OpenAI’s GPT-4 for intelligent code generation, code analysis, and language understanding.
- 🖥️ **Streamlit-Based User Interface**: A user-friendly web interface that allows users to interact with the AI-powered code assistant effortlessly.
- 🛠️ **Support for Multiple Programming Languages**: Provides coding assistance across a variety of programming languages, including Python, JavaScript, Go, and more.

## 🛠 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ai-code-assistant.git
   cd ai-code-assistant
   ```

2. Install the required dependencies for FastAPI, LlamaParse, and OpenAI integrations:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add the following variables:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
   ```

   These keys are required for interacting with the OpenAI and LlamaParse APIs.

## 🚀 Usage

1. **Start the FastAPI server**:

   ```bash
   uvicorn fastapi.main:app --reload
   ```

   This will start the backend service, which handles requests and provides the AI-powered code assistant's functionality.

2. **Run the Streamlit application**:

   ```bash
   streamlit run common/examples/app-streamlit.py
   ```

   The Streamlit app provides a web-based interface where users can interact with the assistant. After launching, access the app at `http://localhost:8501`.

3. **Access the FastAPI docs**:
   Visit `http://localhost:8000/docs` to explore the API endpoints and try out requests using FastAPI's built-in documentation system.

## 🗂️ Project Structure

```bash
GEN-AI-UTILS/
│
├── common/               # Utility scripts for shared functionality
├── fastapi/              # FastAPI backend application code
├── llama-parse/          # Scripts and notebooks for document parsing using LlamaParse
├── openai/               # Utilities for interacting with OpenAI's GPT-4 and vector stores
└── .gitignore            # Git ignore file for excluding files from version control
```

### 📂 Common Utilities

The `common` folder contains helper scripts that are used across various components of the project, such as user interface customization, messaging utilities, and OpenAI interaction.

- **`app-streamlit.py`**: Manages the layout and interactions of the Streamlit-based web application.
- **`custom_css_banner.py`**: Injects custom CSS to modify the web interface's banner.
- **`custom_css_main_page.py`**: Handles CSS injection for customizing the main page of the Streamlit app.
- **`message_utils.py`**: Helper functions for managing and formatting user-facing messages.
- **`openai_utils.py`**: Provides utility functions for interfacing with OpenAI’s GPT-4 API.

### 📂 FastAPI Module

The `fastapi` folder is responsible for managing the backend API of the project, handling incoming requests, and routing them to the appropriate AI models or utilities.

- **`main.py`**: Contains the FastAPI application with all the defined routes, dependencies, and request handlers.
- **`Procfile`**: Specifies how the FastAPI application should be run in production environments (e.g., using Uvicorn).
- **`requirements.txt`**: Lists all Python dependencies required for running the FastAPI server and other components.

### 📂 LlamaParse Utilities

The `llama-parse` folder holds scripts and tools for document parsing, particularly using the LlamaParse framework. It can process complex PDFs and extract structured data, such as financial statements.

- **`01-advanced-RAG-with-LlamaParse.ipynb`**: A Jupyter notebook demonstrating the use of LlamaParse with a retrieval-augmented generation (RAG) model.
- **`02-llama-parse-script-v2.py`**: A Python script for parsing documents and extracting information into markdown format.
- **`NVIDIA-10-Q-AUG.pdf`**: Sample document used for testing LlamaParse’s parsing capabilities.

### 📂 OpenAI Utilities

The `openai` folder contains utilities for interacting with OpenAI’s API and managing vector stores for document retrieval tasks.

- **`batch-update-vector-store-files.ipynb`**: A notebook to update vector stores in bulk for RAG or similar use cases.
- **`openai_assistant_respose.py`**: A script for managing the interaction between OpenAI’s GPT-4 and the user interface, handling responses from the assistant.

## 🤝 Contributing

We welcome contributions to the project! If you’d like to contribute, please fork the repository, make your changes, and submit a pull request. Be sure to follow the code style guidelines and provide adequate documentation.

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this project under the terms of the license.
