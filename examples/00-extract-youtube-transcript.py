import os
import sys
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv

# Import the YouTubeTranscriptApi and specific exceptions
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript


def load_api_key():
    """Load the YOUTUBE_API_KEY from environment variables using python-dotenv."""
    load_dotenv()
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key:
        print("Error: YOUTUBE_API_KEY is not set in the environment variables.")
        sys.exit(1)
    return youtube_api_key


def extract_video_id(youtube_url: str) -> str:
    """Extract the video ID from a given YouTube URL.
    Supports both standard and short URLs.
    """
    try:
        parsed_url = urlparse(youtube_url)
        if 'youtube.com' in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            video_ids = query_params.get('v')
            if video_ids and len(video_ids) > 0:
                return video_ids[0]
            else:
                raise ValueError("Missing video id in URL query parameters")
        elif 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            if video_id:
                # In case the path has extra parts, take only the first segment
                return video_id.split('/')[0]
            else:
                raise ValueError("Missing video id in short URL path")
        else:
            raise ValueError("Invalid YouTube URL")
    except Exception as e:
        raise ValueError(f"Error parsing URL: {e}")


def fetch_transcript(video_id: str) -> str:
    """Fetch the transcript for the given video ID using youtube_transcript_api."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([item.get("text", "") for item in transcript_list])
        return transcript_text
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("No transcript found for this video.")
    except CouldNotRetrieveTranscript as e:
        raise Exception(f"Could not retrieve transcript: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while fetching transcript: {e}")


def main():
    try:
        print("Loading environment variables...")
        load_api_key()  # Ensure API key is loaded, even though it's not used directly here.
        # Use a command-line argument if provided, otherwise prompt the user
        if len(sys.argv) > 1:
            youtube_url = sys.argv[1]
        else:
            youtube_url = input("Enter a YouTube URL: ").strip()
        if not youtube_url:
            print("No URL provided. Exiting.")
            sys.exit(1)
        video_id = extract_video_id(youtube_url)
        print(f"Extracted video ID: {video_id}")
        print("Fetching transcript...")
        transcript = fetch_transcript(video_id)
        
        # Always save to markdown file
        output_file = sys.argv[2] if len(sys.argv) > 2 else "transcript.md"
        markdown_content = f"""# YouTube Transcript

## Video Information
- Video ID: {video_id}
- URL: {youtube_url}

## Transcript Content
```text
{transcript}
```
"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"\nTranscript saved to: {output_file}")
        except Exception as file_err:
            print(f"Error saving transcript to {output_file}: {file_err}")
        
        # Also print to console
        print("\nTranscript content:\n")
        print(transcript)
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
