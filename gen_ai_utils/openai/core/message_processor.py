"""
Message Processor - Consolidated message formatting and processing utilities

This module consolidates all message-related operations from multiple helper scripts
including formatting, extraction, consolidation, and timezone conversion.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import pytz
from colorama import Fore, Style


class MessageProcessor:
    """Processes and formats OpenAI Assistant messages"""

    def __init__(self, timezone: str = "Asia/Bangkok"):
        """
        Initialize MessageProcessor

        Args:
            timezone: Timezone for timestamp conversion
        """
        self.timezone = pytz.timezone(timezone)

    def extract_text_content(self, message: Dict[str, Any]) -> str:
        """
        Extract text content from a message object

        Args:
            message: Message dictionary from OpenAI API

        Returns:
            Extracted text content as string
        """
        content = message.get("content", [])
        text_parts = []

        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_value = part.get("text", {}).get("value", "")
                text_parts.append(text_value)

        return "\n".join(text_parts)

    def convert_to_timezone(self, timestamp: int) -> str:
        """
        Convert Unix timestamp to formatted string in specified timezone

        Args:
            timestamp: Unix timestamp

        Returns:
            Formatted datetime string
        """
        dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
        local_dt = dt.astimezone(self.timezone)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

    def format_message(
        self,
        message: Dict[str, Any],
        include_color: bool = True,
        include_metadata: bool = True
    ) -> str:
        """
        Format a message with color and structure

        Args:
            message: Message dictionary
            include_color: Whether to include color codes
            include_metadata: Whether to include timestamp and metadata

        Returns:
            Formatted message string
        """
        text_content = self.extract_text_content(message)
        role = message.get('role', 'unknown')

        # Set color based on role
        if include_color:
            color = Fore.MAGENTA if role == 'user' else Fore.BLUE
            reset = Style.RESET_ALL
        else:
            color = reset = ""

        formatted_msg = f"{color}"

        if include_metadata:
            created_at = message.get('created_at', 0)
            date_str = self.convert_to_timezone(created_at)
            formatted_msg += f"Time: {date_str}\n"
            formatted_msg += f"Role: {role}\n"

        formatted_msg += f"Content: {text_content}{reset}\n"

        if include_metadata:
            formatted_msg += "=" * 50 + "\n"

        return formatted_msg

    def format_messages(
        self,
        messages: List[Dict[str, Any]],
        sort_by_time: bool = True,
        reverse: bool = False
    ) -> str:
        """
        Format multiple messages into a readable conversation

        Args:
            messages: List of message dictionaries
            sort_by_time: Whether to sort by timestamp
            reverse: Whether to reverse the order

        Returns:
            Formatted conversation string
        """
        if sort_by_time:
            sorted_messages = sorted(
                messages,
                key=lambda x: x.get('created_at', 0),
                reverse=reverse
            )
        else:
            sorted_messages = messages

        formatted_output = "# Conversation Thread\n\n"
        for message in sorted_messages:
            formatted_output += self.format_message(message)

        return formatted_output

    def display_thread_messages(self, messages_response: Any) -> str:
        """
        Display messages from OpenAI API response (legacy compatibility)

        Args:
            messages_response: OpenAI messages list response

        Returns:
            Formatted messages as string
        """
        message_texts = []

        # Handle both API response objects and dictionaries
        if hasattr(messages_response, 'data'):
            messages = messages_response.data
        else:
            messages = messages_response.get('data', [])

        for thread_message in reversed(messages):
            # Extract text content
            if hasattr(thread_message, 'content'):
                content = thread_message.content
            else:
                content = thread_message.get('content', [])

            for part in content:
                if isinstance(part, dict):
                    if part.get('type') == 'text':
                        message_texts.append(part['text']['value'])
                elif hasattr(part, 'text'):
                    message_texts.append(part.text.value)

        return "\n\n".join(message_texts)

    def consolidate_messages(
        self,
        messages: List[Dict[str, Any]],
        role_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Consolidate and filter messages

        Args:
            messages: List of message dictionaries
            role_filter: Filter by role ('user' or 'assistant')

        Returns:
            Filtered and consolidated message list
        """
        consolidated = []

        for message in messages:
            if role_filter and message.get('role') != role_filter:
                continue

            consolidated_message = {
                'id': message.get('id'),
                'created_at': message.get('created_at'),
                'created_at_formatted': self.convert_to_timezone(message.get('created_at', 0)),
                'role': message.get('role'),
                'content': self.extract_text_content(message)
            }

            consolidated.append(consolidated_message)

        return consolidated

    def extract_user_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract only user messages from a conversation

        Args:
            messages: List of message dictionaries

        Returns:
            List of user messages only
        """
        return self.consolidate_messages(messages, role_filter='user')

    def extract_assistant_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract only assistant messages from a conversation

        Args:
            messages: List of message dictionaries

        Returns:
            List of assistant messages only
        """
        return self.consolidate_messages(messages, role_filter='assistant')

    def get_message_stats(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about messages

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary with message statistics
        """
        user_messages = self.extract_user_messages(messages)
        assistant_messages = self.extract_assistant_messages(messages)

        return {
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'first_message_time': self.convert_to_timezone(messages[0].get('created_at', 0)) if messages else None,
            'last_message_time': self.convert_to_timezone(messages[-1].get('created_at', 0)) if messages else None
        }
