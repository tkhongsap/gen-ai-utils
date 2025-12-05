import re

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

def main():
    # Specify the path to your text file
    file_path = 'openai/threads_blob.txt'  # Update the path as needed

    # Extract the thread IDs
    thread_ids = extract_thread_ids(file_path)

    # Output the result
    if thread_ids:
        print("Extracted thread IDs:")
        for thread_id in thread_ids:
            print(thread_id)
    else:
        print("No thread IDs found.")

if __name__ == "__main__":
    main()
