import os
import json
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Define paths
input_dir = Path("openai/output/user_messages")
output_dir = Path("openai/output/user_message_categorization")
output_dir.mkdir(parents=True, exist_ok=True)

# System prompt for message categorization
SYSTEM_PROMPT = """
You are an AI assistant specialized in categorizing user messages to help inform software capability development. For each user message, provide the following in JSON format:

1. **Main Category**: The primary classification of the user's request (e.g., Technical Support, Feature Request, Bug Report, Usability Feedback, General Inquiry, etc.).
2. **Intent Description**: A concise summary of what the user is asking or aiming to achieve.
3. **Relevant Capability Areas**: Identify one or more areas of software development that the request pertains to (e.g., Data Engineering, Data Modeling, Backend, Frontend, Python, Node.js, DevOps, UX/UI Design, etc.).

**Note**:
- Focus on the context and content of the message rather than the urgency.
- Ensure that the categorization aligns with potential capability areas your development team can address.
- If a message pertains to multiple capability areas, list all that apply.

**Format your response as JSON with the following fields:**
```json
{
  "main_category": "string",
  "intent_description": "string",
  "relevant_capability_areas": ["string", "string", ...]
}
"""

def process_file(file_path: Path):
    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    thread_id = data['thread_id']
    messages = data['messages']
    
    # Process each message in the thread
    analyzed_messages = []
    for msg in messages:
        if msg['role'] == 'user':
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": msg['content']}
                    ],
                    stream=False
                )
                
                analysis = response.choices[0].message.content
                print(f"\nOriginal message: {msg['content']}")
                print(f"Analysis: {analysis}")
                
                analyzed_messages.append({
                    "message_id": msg['id'],
                    "timestamp": msg['created_at_formatted'],
                    "content": msg['content'],
                    "analysis": json.loads(analysis)
                })
            except Exception as e:
                print(f"Error processing message {msg['id']}: {str(e)}")
    
    # Save the results
    output_file = output_dir / f"categorized_{thread_id}_{data['date']}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "thread_id": thread_id,
            "date": data['date'],
            "analyzed_messages": analyzed_messages
        }, f, ensure_ascii=False, indent=2)

def main():
    # Process only the first 2 files in the input directory
    for file_path in list(input_dir.glob("*.json"))[:2]:
        print(f"\nProcessing {file_path.name}...")
        try:
            process_file(file_path)
            print(f"Successfully processed {file_path.name}")
        except Exception as e:
            print(f"Error processing file {file_path.name}: {str(e)}")

if __name__ == "__main__":
    main() 