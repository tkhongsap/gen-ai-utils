import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get and print the API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"OpenAI API Key: {api_key}")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def list_pdf_files(directory):
    """List all PDF files in the specified directory."""
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(file)
    return pdf_files

def extract_document_info(pdf_path, query):
    """Extract information from a PDF file using OpenAI's Responses API."""
    try:
        # Upload the file to OpenAI
        with open(pdf_path, "rb") as file_data:
            file = client.files.create(
                file=file_data,
                purpose="user_data"
            )
            
        print(f"File uploaded with ID: {file.id}")
        
        # Create a response using the file
        response = client.responses.create(
            model="gpt-4.1-mini",  # You can change this to your preferred model
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": file.id,
                        },
                        {
                            "type": "input_text",
                            "text": query,
                        },
                    ]
                }
            ]
        )
        
        # Print the response
        result = response.output_text
        
        # Clean up - delete the file after use
        try:
            client.files.delete(file.id)
            print(f"File {file.id} deleted.")
        except Exception as e:
            print(f"Warning: Could not delete file {file.id}: {e}")
            
        return result
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Extract information from PDF files using OpenAI.')
    parser.add_argument('--file', help='Specific PDF file to process (optional)')
    parser.add_argument('--query', default='Summarize this document.', 
                       help='Query to ask about the document (default: "Summarize this document.")')
    args = parser.parse_args()
    
    # Always use 'invoice-07.pdf' from openai/docs as the input PDF
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
    output_dir = docs_dir  # Save output in the docs folder
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Use a detailed extraction prompt for invoices/POs in Thai and English
    extraction_query = (
        "Extract the following information from this document (which may be an invoice or purchase order, in Thai or English):\n"
        "1. company_name\n"
        "2. address\n"
        "3. date\n"
        "4. invoice_numbers_or_po_numbers\n"
        "5. items (a list of objects, each with name, quantity, and price). Extract every item listed in the document, and do not omit any items unless they are crossed out or struck through."
        "   - If an item is crossed out but replaced by another value (e.g., a handwritten correction), only display the replacement value in the output (not the crossed-out one).\n"
        "   - If you are unsure about any item, indicate so.\n"
        "6. total_amount\n"
        "7. other (any additional relevant information not covered above)\n"
        "\nThe document may contain handwritten text. Please carefully extract the information, ignoring any crossed-out or struck-through items.\n"
        "If any item was crossed out but replaced with a handwritten correction, use the new corrected value and exclude the crossed-out version.\n"
        "\nOutput the result as a JSON object with the following fields: company_name, address, date, invoice_numbers_or_po_numbers, items, total_amount, other. The 'items' field should be a list of objects, each with name, quantity, and price.\n"
    )


    pdf_files = ['invoice-07.pdf']
    
    if not pdf_files:
        print(f"No PDF files found in {docs_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_dir, pdf_file)
        print(f"\nProcessing: {pdf_file}")
        
        result = extract_document_info(pdf_path, extraction_query)
        
        if result:
            # Save the result to a text file
            output_filename = f"{os.path.splitext(pdf_file)[0]}_extraction.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            
            print(f"Result saved to {output_path}")
            print(f"Summary: {result[:200]}..." if len(result) > 200 else f"Summary: {result}")
    
    print("\nAll documents processed.")

if __name__ == "__main__":
    main()
