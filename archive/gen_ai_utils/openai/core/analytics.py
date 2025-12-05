"""
Message Analytics - User message categorization and sentiment analysis

This module provides analytics capabilities for OpenAI Assistant messages
including categorization, sentiment analysis, and pattern detection.
"""

from typing import List, Dict, Any, Optional
from collections import Counter
import re


class MessageAnalytics:
    """Analyzes OpenAI Assistant messages for patterns and insights"""

    def __init__(self):
        """Initialize MessageAnalytics"""
        self.categories = {
            'question': r'\?$|^(what|how|why|when|where|who|can|could|would|should|is|are|do|does)',
            'command': r'^(please|kindly|could you|can you|help|fix|create|build|make|generate)',
            'feedback': r'(thank|thanks|great|good|bad|issue|problem|error|bug)',
            'clarification': r'(mean|explain|clarify|understand|confused)',
        }

    def categorize_message(self, content: str) -> str:
        """
        Categorize a message based on its content

        Args:
            content: Message content

        Returns:
            Category name as string
        """
        content_lower = content.lower().strip()

        for category, pattern in self.categories.items():
            if re.search(pattern, content_lower, re.IGNORECASE):
                return category

        return 'statement'

    def categorize_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Categorize multiple messages

        Args:
            messages: List of message dictionaries

        Returns:
            List of messages with added 'category' field
        """
        categorized = []

        for message in messages:
            content = message.get('content', '')
            category = self.categorize_message(content)

            categorized_message = message.copy()
            categorized_message['category'] = category
            categorized.append(categorized_message)

        return categorized

    def get_category_distribution(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get distribution of message categories

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary mapping categories to counts
        """
        categorized = self.categorize_messages(messages)
        categories = [msg['category'] for msg in categorized]
        return dict(Counter(categories))

    def analyze_sentiment(self, content: str) -> str:
        """
        Basic sentiment analysis of message content

        Args:
            content: Message content

        Returns:
            Sentiment ('positive', 'negative', or 'neutral')
        """
        content_lower = content.lower()

        positive_words = ['good', 'great', 'excellent', 'awesome', 'perfect', 'thank', 'thanks', 'helpful', 'love', 'nice']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'problem', 'issue', 'error', 'bug', 'wrong', 'broken', 'fail']

        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def get_sentiment_distribution(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get sentiment distribution across messages

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary mapping sentiments to counts
        """
        sentiments = [self.analyze_sentiment(msg.get('content', '')) for msg in messages]
        return dict(Counter(sentiments))

    def extract_keywords(self, messages: List[Dict[str, Any]], top_n: int = 10) -> List[tuple]:
        """
        Extract top keywords from messages

        Args:
            messages: List of message dictionaries
            top_n: Number of top keywords to return

        Returns:
            List of (keyword, count) tuples
        """
        # Common English stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
            'his', 'her', 'its', 'our', 'their'
        }

        all_words = []
        for message in messages:
            content = message.get('content', '').lower()
            # Extract words (alphanumeric sequences)
            words = re.findall(r'\b[a-z]+\b', content)
            # Filter out stop words and short words
            filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
            all_words.extend(filtered_words)

        word_counts = Counter(all_words)
        return word_counts.most_common(top_n)

    def get_message_length_stats(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about message lengths

        Args:
            messages: List of message dictionaries

        Returns:
            Dictionary with length statistics
        """
        lengths = [len(msg.get('content', '')) for msg in messages]

        if not lengths:
            return {
                'min': 0,
                'max': 0,
                'avg': 0,
                'total': 0
            }

        return {
            'min': min(lengths),
            'max': max(lengths),
            'avg': sum(lengths) / len(lengths),
            'total': sum(lengths)
        }

    def get_conversation_patterns(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze conversation patterns

        Args:
            messages: List of message dictionaries (should be sorted by time)

        Returns:
            Dictionary with pattern insights
        """
        if not messages:
            return {}

        user_msgs = [m for m in messages if m.get('role') == 'user']
        assistant_msgs = [m for m in messages if m.get('role') == 'assistant']

        # Calculate response times (if timestamps available)
        response_times = []
        for i in range(len(messages) - 1):
            if messages[i].get('role') == 'user' and messages[i+1].get('role') == 'assistant':
                time_diff = messages[i+1].get('created_at', 0) - messages[i].get('created_at', 0)
                response_times.append(time_diff)

        return {
            'total_exchanges': min(len(user_msgs), len(assistant_msgs)),
            'user_message_count': len(user_msgs),
            'assistant_message_count': len(assistant_msgs),
            'avg_response_time_seconds': sum(response_times) / len(response_times) if response_times else 0,
            'conversation_duration_seconds': messages[-1].get('created_at', 0) - messages[0].get('created_at', 0) if len(messages) > 1 else 0
        }

    def generate_report(self, messages: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive analytics report

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted report string
        """
        report = "=" * 60 + "\n"
        report += "MESSAGE ANALYTICS REPORT\n"
        report += "=" * 60 + "\n\n"

        # Category distribution
        report += "Category Distribution:\n"
        categories = self.get_category_distribution(messages)
        for category, count in categories.items():
            report += f"  {category.capitalize()}: {count}\n"
        report += "\n"

        # Sentiment distribution
        report += "Sentiment Distribution:\n"
        sentiments = self.get_sentiment_distribution(messages)
        for sentiment, count in sentiments.items():
            report += f"  {sentiment.capitalize()}: {count}\n"
        report += "\n"

        # Top keywords
        report += "Top Keywords:\n"
        keywords = self.extract_keywords(messages, top_n=10)
        for word, count in keywords:
            report += f"  {word}: {count}\n"
        report += "\n"

        # Length statistics
        report += "Message Length Statistics:\n"
        length_stats = self.get_message_length_stats(messages)
        report += f"  Min: {length_stats['min']} characters\n"
        report += f"  Max: {length_stats['max']} characters\n"
        report += f"  Average: {length_stats['avg']:.2f} characters\n"
        report += "\n"

        # Conversation patterns
        report += "Conversation Patterns:\n"
        patterns = self.get_conversation_patterns(messages)
        for key, value in patterns.items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"
        report += "\n"

        report += "=" * 60 + "\n"

        return report
