from pathlib import Path
from datetime import datetime
import re

def read_markdown_files(output_dir):
    """Read all markdown files from the output directory"""
    # Only get files that start with 'thread_' and end with '.md'
    markdown_files = list(Path(output_dir).glob('thread_*.md'))
    # Sort files by creation time
    markdown_files.sort(key=lambda x: x.stat().st_ctime)
    return markdown_files

def extract_thread_id(filename):
    """Extract thread ID from filename"""
    match = re.search(r'thread_(thread_\w+)_\d+', filename.name)
    return match.group(1) if match else None

def consolidate_markdown_files(output_dir):
    """Consolidate all markdown files into a single file"""
    # Get all markdown files
    markdown_files = read_markdown_files(output_dir)
    
    if not markdown_files:
        print("No markdown files found to consolidate.")
        return
    
    print(f"Found {len(markdown_files)} markdown files to consolidate.")
    
    # Create the consolidated content
    consolidated_content = "# Consolidated OpenAI Conversations\n\n"
    consolidated_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    consolidated_content += f"Total Conversations: {len(markdown_files)}\n\n"
    
    # Process each file
    for file_path in markdown_files:
        try:
            # Extract thread ID
            thread_id = extract_thread_id(file_path)
            if not thread_id:
                continue
                
            print(f"Processing: {file_path.name}")
            
            # Read the content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add thread separator and content
            consolidated_content += f"\n## Thread: {thread_id}\n\n"
            consolidated_content += content
            consolidated_content += "\n" + "=" * 80 + "\n"  # Add separator between threads
            
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
    
    # Save consolidated content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"consolidated_threads_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(consolidated_content)
    
    print(f"\nConsolidated output saved to: {output_file}")

def main():
    # Specify the output directory
    output_dir = "openai/output"
    
    # Consolidate markdown files
    consolidate_markdown_files(output_dir)
    
    print("\nConsolidation completed!")

if __name__ == "__main__":
    main()
