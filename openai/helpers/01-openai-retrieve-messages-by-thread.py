import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from colorama import init, Fore, Style
from pathlib import Path

# Initialize colorama for Windows support
init()

# Load environment variables from .env file
load_dotenv()

# Base URL for the API
BASE_URL = "https://api.openai.com/v1"

# Load the API key from the .env file
API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure OPENAI_API_KEY exists in your .env file

if not API_KEY:
    raise ValueError("API key not found. Please set OPENAI_API_KEY in the .env file.")

# Headers for authentication and beta features
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2"
}

# Function to retrieve a thread
def retrieve_thread(thread_id):
    url = f"{BASE_URL}/threads/{thread_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving thread: {response.status_code}, {response.text}")
        return None

# Function to extract and display messages from a thread
def extract_messages(thread_id, limit=20, order="asc"):
    url = f"{BASE_URL}/threads/{thread_id}/messages?limit={limit}&order={order}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error extracting messages: {response.status_code}, {response.text}")
        return None

def format_message(message_data):
    """Format a single message with color and structure"""
    # Extract the text content from the message structure
    content = message_data.get("content", [])
    text_content = ""
    for part in content:
        if part["type"] == "text":
            text_content = part["text"]["value"]
    
    # Convert timestamp to readable date
    created_at = datetime.fromtimestamp(message_data.get('created_at', 0))
    date_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    # Set color based on role
    color = Fore.MAGENTA if message_data['role'] == 'user' else Fore.BLUE
    
    # Format the message
    formatted_msg = f"{color}Time: {date_str}\n"
    formatted_msg += f"Role: {message_data['role']}\n"
    formatted_msg += f"Content: {text_content}{Style.RESET_ALL}\n"
    formatted_msg += "=" * 50 + "\n"  # Divider
    
    return formatted_msg

def process_thread_messages(messages_data):
    """Process and sort thread messages"""
    try:
        # Extract messages and sort by created_at
        messages = messages_data.get('data', [])
        sorted_messages = sorted(messages, key=lambda x: x.get('created_at', 0))
        
        # Format each message
        formatted_output = "# Conversation Thread\n\n"
        for message in sorted_messages:
            formatted_output += format_message(message)
        
        return formatted_output
        
    except Exception as e:
        return f"Error processing messages: {str(e)}"

def save_to_markdown(thread_id, formatted_output):
    """Save the formatted output to a markdown file"""
    # Create output directory if it doesn't exist
    output_dir = Path("openai/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"thread_{thread_id}_{timestamp}.md"
    
    # Save the formatted output
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_output)
    
    print(f"\nOutput saved to: {output_path}")

def save_to_json(thread_id, messages_data):
    """Save the raw messages data to a JSON file"""
    # Create output directory if it doesn't exist
    output_dir = Path("openai/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"thread_{thread_id}_{timestamp}.json"
    
    # Prepare JSON data with better structure
    output_data = {
        "thread_id": thread_id,
        "timestamp": timestamp,
        "messages": []
    }
    
    # Process each message
    for message in messages_data.get('data', []):
        # Extract text content
        content = message.get("content", [])
        text_content = ""
        for part in content:
            if part["type"] == "text":
                text_content = part["text"]["value"]
        
        # Create message entry
        message_entry = {
            "id": message.get("id"),
            "created_at": message.get("created_at"),
            "created_at_formatted": datetime.fromtimestamp(message.get('created_at', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            "role": message.get("role"),
            "content": text_content
        }
        output_data["messages"].append(message_entry)
    
    # Save the JSON file
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nJSON output saved to: {output_path}")

def read_thread_ids(file_path):
    """Read thread IDs from the specified file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read lines and remove any whitespace/newlines
            thread_ids = [line.strip() for line in f if line.strip()]
        return thread_ids
    except FileNotFoundError:
        print(f"Thread IDs file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading thread IDs file: {e}")
        return []

def process_thread(thread_id):
    """Process a single thread"""
    print(f"\nProcessing thread: {thread_id}")
    
    # Get messages from the thread
    messages_data = extract_messages(thread_id)
    
    if messages_data:
        # Format and save as markdown for human reading
        formatted_output = process_thread_messages(messages_data)
        print(formatted_output)
        save_to_markdown(thread_id, formatted_output)
        
        # Save raw data as JSON for processing
        save_to_json(thread_id, messages_data)
        
        print(f"Completed processing thread: {thread_id}")
    else:
        print(f"No messages found for thread: {thread_id}")

def main():
    # Specify the path to the thread IDs file
    thread_ids_file = "openai/output/thread_ids_20241120_132336.txt"
    
    # Read thread IDs
    thread_ids = read_thread_ids(thread_ids_file)
    
    if not thread_ids:
        print("No thread IDs found to process.")
        return
    
    print(f"Found {len(thread_ids)} threads to process")
    
    # Process each thread
    for i, thread_id in enumerate(thread_ids, 1):
        print(f"\nProcessing thread {i} of {len(thread_ids)}")
        process_thread(thread_id)
        
    print("\nAll threads processed successfully!")

if __name__ == "__main__":
    main()
