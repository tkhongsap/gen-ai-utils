"""
This script extracts OpenAI thread IDs from a text file and saves them to a separate output file.
It specifically looks for IDs that start with 'thread_' followed by alphanumeric characters.

The script:
1. Reads from a source file (threads_blob.txt)
2. Extracts all thread IDs using regex
3. Saves the extracted IDs to a timestamped file in the openai/output directory
4. Prints the extracted IDs to the console
"""

import re
from pathlib import Path
from datetime import datetime

def extract_thread_ids(file_path):
    """
    Extract thread IDs that start with "thread_" from the provided text file.
    """
    try:
        # Open and read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Use regex to find all occurrences of thread_ followed by alphanumeric characters
        thread_ids = re.findall(r'thread_\w+', content)

        return thread_ids
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def save_thread_ids(thread_ids):
    """
    Save thread IDs to a text file in the openai/output directory
    """
    # Create output directory if it doesn't exist
    output_dir = Path("openai/output/thread_ids")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"thread_ids_{timestamp}.txt"
    output_path = output_dir / filename
    
    # Save the thread IDs
    with open(output_path, 'w', encoding='utf-8') as file:
        for thread_id in thread_ids:
            file.write(f"{thread_id}\n")
    
    print(f"\nThread IDs saved to: {output_path}")

def main():
    # Specify the path to your text file
    file_path = 'openai/threads_blob.txt'  # Update the path as needed

    # Extract the thread IDs
    thread_ids = extract_thread_ids(file_path)

    # Output the result to console
    if thread_ids:
        print("Extracted thread IDs:")
        for thread_id in thread_ids:
            print(thread_id)
        
        # Save thread IDs to file
        save_thread_ids(thread_ids)
    else:
        print("No thread IDs found.")

if __name__ == "__main__":
    main()
