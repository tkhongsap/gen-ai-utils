"""
Thread Manager - Consolidated OpenAI thread operations

This module consolidates all thread-related operations from multiple helper scripts
into a single, well-structured class with proper error handling and type hints.
"""

import time
from typing import Optional, List, Dict, Any
from openai import OpenAI
from datetime import datetime
import json
from pathlib import Path


class ThreadManager:
    """Manages OpenAI Assistant threads with create, retrieve, list, and message operations"""

    def __init__(self, api_key: str, beta_version: str = "assistants=v2"):
        """
        Initialize ThreadManager with OpenAI client

        Args:
            api_key: OpenAI API key
            beta_version: OpenAI beta version header
        """
        self.client = OpenAI(api_key=api_key)
        self.beta_version = beta_version

    def create_thread(self) -> str:
        """
        Create a new thread

        Returns:
            Thread ID as string
        """
        thread = self.client.beta.threads.create()
        return thread.id

    def retrieve_thread(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a thread by ID

        Args:
            thread_id: Thread ID to retrieve

        Returns:
            Thread data as dictionary or None if error
        """
        try:
            thread = self.client.beta.threads.retrieve(thread_id=thread_id)
            return thread.model_dump() if hasattr(thread, 'model_dump') else dict(thread)
        except Exception as e:
            print(f"Error retrieving thread {thread_id}: {str(e)}")
            return None

    def list_threads(self, limit: int = 20) -> List[str]:
        """
        List thread IDs (Note: OpenAI doesn't have a direct list endpoint,
        this would need to be tracked separately)

        Args:
            limit: Maximum number of threads to return

        Returns:
            List of thread IDs
        """
        # Note: OpenAI API doesn't provide a direct way to list all threads
        # Thread IDs should be stored separately (e.g., in a file or database)
        print("Note: Thread listing requires separate storage of thread IDs")
        return []

    def add_message(
        self,
        thread_id: str,
        content: str,
        role: str = "user",
        file_ids: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Add a message to a thread

        Args:
            thread_id: Thread ID to add message to
            content: Message content
            role: Message role (user or assistant)
            file_ids: Optional list of file IDs to attach

        Returns:
            Message ID or None if error
        """
        try:
            message_params = {
                "thread_id": thread_id,
                "role": role,
                "content": content
            }

            if file_ids:
                message_params["file_ids"] = file_ids

            message = self.client.beta.threads.messages.create(**message_params)
            return message.id
        except Exception as e:
            print(f"Error adding message to thread {thread_id}: {str(e)}")
            return None

    def get_messages(
        self,
        thread_id: str,
        limit: int = 20,
        order: str = "asc",
        after: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve messages from a thread

        Args:
            thread_id: Thread ID to retrieve messages from
            limit: Maximum number of messages to return
            order: Sort order ('asc' or 'desc')
            after: Return messages after this message ID

        Returns:
            List of message dictionaries or None if error
        """
        try:
            params = {
                "thread_id": thread_id,
                "limit": limit,
                "order": order
            }

            if after:
                params["after"] = after

            messages = self.client.beta.threads.messages.list(**params)
            return [msg.model_dump() if hasattr(msg, 'model_dump') else dict(msg)
                    for msg in messages.data]
        except Exception as e:
            print(f"Error retrieving messages from thread {thread_id}: {str(e)}")
            return None

    def run_assistant(
        self,
        thread_id: str,
        assistant_id: str,
        instructions: Optional[str] = None
    ) -> Optional[str]:
        """
        Run an assistant on a thread

        Args:
            thread_id: Thread ID to run assistant on
            assistant_id: Assistant ID to use
            instructions: Optional additional instructions

        Returns:
            Run ID or None if error
        """
        try:
            run_params = {
                "thread_id": thread_id,
                "assistant_id": assistant_id
            }

            if instructions:
                run_params["instructions"] = instructions

            run = self.client.beta.threads.runs.create(**run_params)
            return run.id
        except Exception as e:
            print(f"Error running assistant on thread {thread_id}: {str(e)}")
            return None

    def wait_on_run(
        self,
        thread_id: str,
        run_id: str,
        poll_interval: float = 0.5,
        timeout: int = 300
    ) -> Optional[str]:
        """
        Wait for a run to complete

        Args:
            thread_id: Thread ID
            run_id: Run ID to wait for
            poll_interval: Seconds between status checks
            timeout: Maximum seconds to wait

        Returns:
            Final run status or None if timeout/error
        """
        start_time = time.time()

        try:
            while time.time() - start_time < timeout:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )

                if run.status in ['completed', 'failed', 'cancelled', 'expired']:
                    return run.status

                time.sleep(poll_interval)

            print(f"Timeout waiting for run {run_id}")
            return None
        except Exception as e:
            print(f"Error waiting on run {run_id}: {str(e)}")
            return None

    def save_thread_ids(self, thread_ids: List[str], output_dir: str = "openai/output/thread_ids") -> str:
        """
        Save thread IDs to a file

        Args:
            thread_ids: List of thread IDs to save
            output_dir: Directory to save file

        Returns:
            Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thread_ids_{timestamp}.txt"
        filepath = output_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            for thread_id in thread_ids:
                f.write(f"{thread_id}\n")

        return str(filepath)

    def load_thread_ids(self, filepath: str) -> List[str]:
        """
        Load thread IDs from a file

        Args:
            filepath: Path to file containing thread IDs

        Returns:
            List of thread IDs
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Thread IDs file not found: {filepath}")
            return []
        except Exception as e:
            print(f"Error reading thread IDs file: {e}")
            return []
