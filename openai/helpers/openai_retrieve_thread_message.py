import os
import requests
import json
from datetime import datetime, timezone, timedelta

# Load API Key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://api.openai.com/v1"

# Set the specific assistant and thread IDs
ASSISTANT_ID = "asst_CsRUOSckEYjuORKgVduj9Yib"  # Replace with your specific assistant ID
THREAD_ID = "thread_QbMqmPShmMXVnKWaAR1md8w5"    # Replace with your specific thread ID

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

def main():
    # Retrieve messages for the specific thread ID
    print(f"Retrieving messages for thread {THREAD_ID}...")
    messages_data = get_thread_messages(THREAD_ID)
    
    if messages_data:
        # Prepare a list to hold message information in JSON format
        message_list = []
        
        # The messages are under the "data" field
        messages = messages_data.get("data", [])
        
        for message in messages:
            message_id = message.get("id")
            role = message.get("role", "unknown")
            assistant_id = message.get("assistant_id", ASSISTANT_ID)  # Use thread assistant_id if message lacks it
            thread_id = message.get("thread_id", THREAD_ID)
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
        
        # Output the list of messages as JSON
        print(json.dumps(message_list, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
