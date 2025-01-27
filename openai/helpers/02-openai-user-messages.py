"""
OpenAI User Messages Extractor

This script processes JSON files in the thread_ids_messages folder and:
1. Reads each JSON file containing thread messages
2. Filters messages to keep only those with "role": "user"
3. Saves filtered messages to new JSON files in openai/output/user_messages/
   using similar naming convention

The script requires:
- Input: JSON files in openai/output/thread_ids_messages/
- Output: Filtered JSON files in openai/output/user_messages/
"""

import json
from pathlib import Path
import sys
from datetime import datetime

def process_thread_file(input_file: Path) -> dict:
    """
    Process a single thread file and extract user messages.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            thread_data = json.load(f)
        
        # Create new data structure with only user messages
        filtered_data = {
            "thread_id": thread_data["thread_id"],
            "date": thread_data["timestamp"],  # Changed to 'date' here
            "messages": [
                msg for msg in thread_data["messages"]
                if msg["role"] == "user"
            ]
        }
        
        return filtered_data
    
    except Exception as e:
        print(f"Error processing file {input_file}: {str(e)}")
        return None

def save_filtered_messages(filtered_data: dict, output_path: Path):
    """
    Save filtered messages to JSON file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        print(f"Saved filtered messages to: {output_path}")
    
    except Exception as e:
        print(f"Error saving to {output_path}: {str(e)}")

def main():
    # Setup input and output directories
    input_dir = Path("openai/output/thread_ids_messages")
    output_dir = Path("openai/output/user_messages")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all JSON files in input directory
    json_files = list(input_dir.glob("*.json"))
    
    if not json_files:
        print("No JSON files found in input directory")
        sys.exit(1)
    
    print(f"Found {len(json_files)} files to process")
    print("\nStarting processing...")
    
    # Process each file
    for input_file in json_files:
        print(f"\n{'='*50}")
        print(f"Processing: {input_file.name}")
        
        # Process the file
        filtered_data = process_thread_file(input_file)
        
        if filtered_data:
            # Create output file with modified name format
            output_filename = f"messages_{filtered_data['thread_id']}_{filtered_data['date']}.json"
            output_path = output_dir / output_filename
            
            # Save filtered messages
            save_filtered_messages(filtered_data, output_path)
            
            # Print summary
            user_msg_count = len(filtered_data["messages"])
            print(f"Extracted {user_msg_count} user messages")
            print(f"First user message preview: {filtered_data['messages'][0]['content'][:100]}...")
        
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()
