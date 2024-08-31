
# 🧠 Gen-AI Utils

A comprehensive collection of utility scripts and helper functions designed to streamline your work with various generative AI APIs, including OpenAI, Anthropic, and others. This repository provides reusable components and examples that make it easy to integrate and manage generative AI capabilities in your projects.

## 🚀 Features

- **🛠️ Generative AI Utilities**:
  - Unified scripts for interacting with multiple generative AI APIs, such as OpenAI and Anthropic.
  - Includes functions for managing files, chat interactions, and vector store operations.
  - Customizable scripts for generating responses, processing prompts, and handling API-specific tasks.

- **🔧 Common Utilities**:
  - Environment management, logging, and request handling utilities that can be shared across different AI APIs.
  - Custom CSS for enhancing the appearance of Streamlit applications, making your interfaces more user-friendly and visually appealing.

## 📦 Installation

To get started with these utilities, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/yourusername/gen-ai-utils.git
cd gen-ai-utils
pip install -r requirements.txt
```

Make sure to set up your environment variables, particularly API keys for the generative AI services you're using. You can use a `.env` file to securely manage these variables.

## 📁 Directory Structure

The repository is organized to support multiple AI APIs, with a clear separation of utilities and examples:

```plaintext
gen-ai-utils/
│
├── app-streamlit.py                       # Example Streamlit app demonstrating usage
├── generative_ai/
│   ├── openai/
│   │   ├── batch-update-vector-store-files.ipynb   # Jupyter notebook for OpenAI vector store batch updates
│   │   ├── delete_vector_store_files.ipynb         # Jupyter notebook for OpenAI vector store file deletion
│   │   ├── openai_assistant_response.py       # Script for generating responses using OpenAI Assistant API
│   │   ├── openai_utils.py                    # Utility functions for interacting with OpenAI API
│   │
│   ├── anthropic/
│   │   └── anthropic_utils.py                 # Placeholder for Anthropic-specific utilities
│   │
│   ├── gemini/                                # Placeholder for Gemini API utilities
│   ├── llama/                                 # Placeholder for LLaMA API utilities
│
├── utils/
│   ├── custom_css_main_page.py            # Custom CSS for the main page styling
│   ├── custom_css_banner.py               # Custom CSS for the banner
│   ├── message_utils.py                   # Utility functions for formatting and displaying messages
│
├── .gitignore                             # Git ignore file
├── LICENSE                                # License for the repository
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
└── .env.example                           # Example environment variables file
```

## ⚙️ Usage

### Generative AI Utilities

#### 💬 Generating a Response

To generate a response using a generative AI API (e.g., OpenAI):

```python
from generative_ai.openai.openai_utils import generate_assistant_response

# Generate a response using OpenAI's Assistant API
response = generate_assistant_response("What's the weather today?", "your_assistant_id")
print(response)
```

#### 🗃️ Managing Vector Stores

For managing vector stores with OpenAI:

- **Batch Update**: Use `batch-update-vector-store-files.ipynb` to update multiple files in a vector store.
- **File Deletion**: Use `delete_vector_store_files.ipynb` to delete files from a vector store.

### 🌐 Streamlit Example

Run the example Streamlit app `app-streamlit.py` to see how these utilities can be integrated into a web application:

```bash
streamlit run app-streamlit.py
```

The app showcases chat interactions using OpenAI's API, enhanced with custom CSS and message formatting utilities.

### 🎨 Common Utilities

- **Custom CSS**: Use `custom_css_main_page.py` and `custom_css_banner.py` to style your Streamlit apps.
- **Message Formatting**: Use `message_utils.py` for consistent formatting and display of chat messages.

## 🤝 Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For any questions or suggestions, feel free to open an issue or contact the repository owner.
