import os
import requests
import json
import re
from datetime import datetime, timezone, timedelta

# Load API Key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://api.openai.com/v1"

# Set the specific assistant ID
ASSISTANT_ID = "asst_CsRUOSckEYjuORKgVduj9Yib"  # Replace with your specific assistant ID

# Headers with authorization
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2"
}

# Helper function to convert Unix timestamp to Bangkok time
def convert_to_bangkok_time(unix_timestamp):
    # Bangkok time is UTC+7
    bangkok_timezone = timezone(timedelta(hours=7))
    dt = datetime.fromtimestamp(unix_timestamp, bangkok_timezone)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

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

def get_thread_messages(thread_id):
    """
    Retrieve all messages for a specific thread.
    """
    messages_url = f"{BASE_URL}/threads/{thread_id}/messages"
    response = requests.get(messages_url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve messages for thread {thread_id}: {response.status_code}, {response.text}")
        return None

def save_output_to_file(output_data, output_path):
    """
    Save the retrieved thread messages to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(output_data, output_file, indent=4, ensure_ascii=False)
        print(f"Output successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save output: {str(e)}")

def process_threads_and_messages(file_path):
    """
    Extract thread IDs from the file and retrieve messages for each thread.
    """
    # Extract thread IDs from the given file
    thread_ids = extract_thread_ids(file_path)
    
    if not thread_ids:
        print("No thread IDs found.")
        return
    
    all_threads_data = []  # To store messages from all threads
    thread_count = 0       # Counter for the number of processed threads

    # Iterate over each thread ID and retrieve messages
    for thread_id in thread_ids:
        print(f"Retrieving messages for thread {thread_id}...")
        messages_data = get_thread_messages(thread_id)
        
        if messages_data:
            # Increment the thread counter
            thread_count += 1

            # Prepare a list to hold message information in JSON format
            message_list = []
            
            # The messages are under the "data" field
            messages = messages_data.get("data", [])
            
            for message in messages:
                message_id = message.get("id")
                role = message.get("role", "unknown")
                assistant_id = message.get("assistant_id", ASSISTANT_ID)  # Use thread assistant_id if message lacks it
                thread_id = message.get("thread_id", thread_id)
                created_at = message.get("created_at")
                created_at_bangkok = convert_to_bangkok_time(created_at)
                message_content = message.get("content", [])
                
                # Extract the actual text content from the message
                text_content = ""
                for content in message_content:
                    if content["type"] == "text":
                        text_content = content["text"]["value"]
                
                # Create a dictionary to represent this message
                message_info = {
                    "assistant_id": assistant_id,  # Include assistant_id in every message
                    "message_id": message_id,
                    "role": role,
                    "thread_id": thread_id,
                    "created_at_unix": created_at,
                    "created_at_bangkok": created_at_bangkok,
                    "content": text_content
                }
                
                # Add this message info to the list
                message_list.append(message_info)
            
            # Store the messages for this thread
            all_threads_data.append({
                "thread_id": thread_id,
                "messages": message_list
            })

    # Define the output file path in the same directory as the input file
    output_path = os.path.join(os.path.dirname(file_path), "retrieved_thread_messages.json")
    
    # Save the list of messages as JSON to a file
    save_output_to_file(all_threads_data, output_path)

    # Print the total number of threads processed
    print(f"Total threads processed: {thread_count}")

if __name__ == "__main__":
    # Path to your threads_blob.txt file
    file_path = 'openai/threads_blob.txt'  # Adjust the path accordingly
    process_threads_and_messages(file_path)
