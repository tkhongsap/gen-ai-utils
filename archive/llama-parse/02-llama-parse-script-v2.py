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

# initial setup 
file_extractor = {".txt": parser}
base_dir = r'D:\#Generative AI\Retrieval Augmented Generation (RAG)\01-Use-Case-Call-Center-Agent'
input_dir = os.path.join(base_dir, 'demo-data', 'test')
output_dir = os.path.join(base_dir, 'output')

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

parsingInstructionMangaLatex = """The text document provided is a result from web-scraping script, which we aim to extract all the information on that particular page. The content is related to a smart city called One Bangkok which is a newly developed real-estate property in the heart of Bangkok where sustainability and community are the core themes of the city. Please extract all the information and organize it is a comprehensive way, we will use this information for FAQs as well as to support our Call Center to answer any queries from our customers.  """

parser = LlamaParse(
    api_key=llama_cloud_api_key,
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction=parsingInstructionMangaLatex 
)

file_extractor = {".txt": parser}
documemnts = parser.load_data("./onebangkok_workplace.txt.txt")


print(documemnts)
print_and_save_documents(documemnts, 'onebangkok_workplace.txt.txt', output_dir)
