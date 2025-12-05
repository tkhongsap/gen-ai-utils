from dotenv import load_dotenv # type: ignore
from os import environ
from os.path import join, splitext, basename

import os

from llama_parse import LlamaParse  # pip install llama-parse
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
from os import environ
from os.path import join

# Load environment variables
load_dotenv()
llama_cloud_api_key = environ.get("LLAMA_CLOUD_API_KEY")
print(llama_cloud_api_key)

# Define the parser and directory reader


parsingInstructionMangaLatex = """The text document provided is a result from web-scraping script, which we aim to extract all the information on that particular page. The content is related to a smart city called One Bangkok which is a newly developed real-estate property in the heart of Bangkok where sustainability and community are the core themes of the city. Please extract all the information and organize it is a comprehensive way, we will use this information for FAQs as well as to support our Call Center to answer any queries from our customers.  """

parser = LlamaParse(
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction=parsingInstructionMangaLatex 
)

# Use SimpleDirectoryReader to parse our file
file_extractor = {".txt": parser}
input_dir = r'D:\#Generative AI\Retrieval Augmented Generation (RAG)\01-Use-Case-Call-Center-Agent\demo-data'
# file_path = join(input_dir, 'Prompt Engineering Guide, 2024-05.pdf')

documents = SimpleDirectoryReader(input_dir, file_extractor=file_extractor).load_data()

# Function to print and save document text with similar naming
def print_and_save_documents(documents, input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = splitext(basename(input_file))[0]
    print(f"Base name: {base_name}")  # Debug print
    print(f"Total number of documents: {len(documents)}")  # Debug print

    for i, doc in enumerate(documents):
        print(f"Processing document {i}")  # Debug print
        text_content = doc.text  # Extract text content from the document
        output_file_name = f"LlamaParse - {base_name}_{i}.md"
        print(f"Output file name: {output_file_name}")  # Debug print
        with open(join(output_folder, output_file_name), "w", encoding="utf-8") as f:
            f.write(text_content)

# Define the output folder and save documents
output_folder = r'D:\#Generative AI\Retrieval Augmented Generation (RAG)\01-Use-Case-Call-Center-Agent\outputt'
print_and_save_documents(documents, file_path, output_folder)