import os
from os import environ
from os.path import join, splitext, basename
from llama_parse import LlamaParse
from dotenv import load_dotenv  # type: ignore

# Load environment variables
load_dotenv()
llama_cloud_api_key = environ.get("LLAMA_CLOUD_API_KEY")
print(llama_cloud_api_key)

# Updated parsing instructions to exclude CSS or any HTML-like content
parsingInstructionNVIDIA = """
The provided document is an NVIDIA 10-Q report containing financial statements, management discussions, and various tables and charts. 
Please carefully extract all the detailed financial information, key figures, tables, and management insights. 
Avoid including any CSS, HTML, or formatting styles like body tags, font families, or inline styles in the extracted content. 
Focus purely on the text and tabular data in a clean markdown format.
"""

parser = LlamaParse(
    api_key=llama_cloud_api_key,
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction=parsingInstructionNVIDIA
)

# Define the file path and data directory
file_path = "./data/NVIDIA-10-Q-AUG.pdf"

# sync
documents = parser.load_data(file_path)

# Function to save all documents into a single markdown file with the desired name
def save_combined_documents(documents, input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate the output file name (same as input name but with .md extension)
    base_name = splitext(basename(input_file))[0]  # Extracts "NVIDIA-10-Q-AUG"
    output_file_name = f"{base_name}.md"  # Set file name to "NVIDIA-10-Q-AUG.md"
    output_path = join(output_folder, output_file_name)

    print(f"Saving all documents to: {output_path}")

    # Combine all document texts into one string
    combined_text = "\n\n".join([doc.text for doc in documents])

    # Write the combined text to a single markdown file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"All documents have been saved to {output_file_name}")

# Define the output folder and save the combined documents
output_folder = "./parse_output"
save_combined_documents(documents, file_path, output_folder)

print("All documents have been saved successfully.")
