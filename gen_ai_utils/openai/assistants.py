"""
Assistant Manager - High-level interface for OpenAI Assistants

This module provides a simplified interface for working with OpenAI Assistants,
combining thread management, message processing, and run execution.
"""

from typing import Optional, Callable, Any
from openai import OpenAI
from gen_ai_utils.openai.core.thread_manager import ThreadManager
from gen_ai_utils.openai.core.message_processor import MessageProcessor


class AssistantManager:
    """High-level manager for OpenAI Assistant interactions"""

    def __init__(
        self,
        api_key: str,
        assistant_id: str,
        timezone: str = "Asia/Bangkok"
    ):
        """
        Initialize AssistantManager

        Args:
            api_key: OpenAI API key
            assistant_id: Assistant ID to use
            timezone: Timezone for message timestamps
        """
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id
        self.thread_manager = ThreadManager(api_key)
        self.message_processor = MessageProcessor(timezone)
        self.current_thread_id: Optional[str] = None

    def create_conversation(self) -> str:
        """
        Create a new conversation thread

        Returns:
            Thread ID
        """
        self.current_thread_id = self.thread_manager.create_thread()
        return self.current_thread_id

    def send_message(
        self,
        content: str,
        thread_id: Optional[str] = None,
        file_ids: Optional[list] = None,
        wait_for_response: bool = True,
        poll_interval: float = 0.5,
        timeout: int = 300
    ) -> Optional[str]:
        """
        Send a message and optionally wait for response

        Args:
            content: Message content
            thread_id: Thread ID (uses current if not specified)
            file_ids: Optional file IDs to attach
            wait_for_response: Whether to wait for assistant response
            poll_interval: Polling interval in seconds
            timeout: Maximum wait time in seconds

        Returns:
            Assistant response text or None
        """
        # Use current thread or specified thread
        thread_id = thread_id or self.current_thread_id

        if not thread_id:
            raise ValueError("No thread ID specified and no current thread")

        # Add user message
        message_id = self.thread_manager.add_message(
            thread_id=thread_id,
            content=content,
            role="user",
            file_ids=file_ids
        )

        if not message_id:
            return None

        if not wait_for_response:
            return None

        # Run assistant
        run_id = self.thread_manager.run_assistant(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )

        if not run_id:
            return None

        # Wait for completion
        status = self.thread_manager.wait_on_run(
            thread_id=thread_id,
            run_id=run_id,
            poll_interval=poll_interval,
            timeout=timeout
        )

        if status != 'completed':
            print(f"Run ended with status: {status}")
            return None

        # Get response messages
        messages = self.thread_manager.get_messages(
            thread_id=thread_id,
            order='desc',
            after=message_id,
            limit=1
        )

        if not messages:
            return None

        # Extract and return response text
        return self.message_processor.extract_text_content(messages[0])

    def get_conversation_history(
        self,
        thread_id: Optional[str] = None,
        formatted: bool = True
    ) -> str:
        """
        Get conversation history

        Args:
            thread_id: Thread ID (uses current if not specified)
            formatted: Whether to return formatted text

        Returns:
            Conversation history as string
        """
        thread_id = thread_id or self.current_thread_id

        if not thread_id:
            raise ValueError("No thread ID specified and no current thread")

        messages = self.thread_manager.get_messages(
            thread_id=thread_id,
            limit=100,
            order='asc'
        )

        if not messages:
            return ""

        if formatted:
            return self.message_processor.format_messages(messages)
        else:
            return "\n\n".join([
                self.message_processor.extract_text_content(msg)
                for msg in messages
            ])

    def stream_response(
        self,
        content: str,
        thread_id: Optional[str] = None,
        callback: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        Send message and stream the response (if supported)

        Args:
            content: Message content
            thread_id: Thread ID (uses current if not specified)
            callback: Optional callback function called with each chunk

        Returns:
            Full response text
        """
        # Note: Streaming implementation depends on OpenAI API version
        # This is a placeholder for the interface
        thread_id = thread_id or self.current_thread_id

        if not thread_id:
            raise ValueError("No thread ID specified and no current thread")

        # For now, use non-streaming approach
        response = self.send_message(content, thread_id=thread_id)

        if callback and response:
            callback(response)

        return response or ""

    def clear_conversation(self):
        """Clear the current conversation thread"""
        self.current_thread_id = None

    def switch_assistant(self, assistant_id: str):
        """
        Switch to a different assistant

        Args:
            assistant_id: New assistant ID
        """
        self.assistant_id = assistant_id
