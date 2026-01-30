"""LLM-based email analysis using Claude."""

import os
from typing import Optional

import anthropic

from src.models.email import Email


class EmailAnalyzer:
    """Analyzes emails using Claude to answer user questions."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def analyze(
        self,
        emails: list[Email],
        question: str,
        include_full_body: bool = False,
    ) -> str:
        """
        Analyze emails and answer a question about them.

        Args:
            emails: List of emails to analyze
            question: User's question about the emails
            include_full_body: Include full email bodies (uses more tokens)

        Returns:
            Analysis response from Claude
        """
        # Format emails for the prompt
        email_content = self._format_emails_for_prompt(emails, include_full_body)

        system_prompt = """You are an email analysis assistant. You have access to a user's emails and will answer their questions about the content.

Guidelines:
- Be specific and cite relevant emails when possible (mention sender, date, subject)
- If the question asks for a list (e.g., "all jobs I applied to"), format the response as a clear list
- If you can't find relevant information, say so clearly
- Respect privacy - only report on information present in the emails
- For job-related queries, look for application confirmations, rejections, interview invites, etc.
- Be concise but thorough"""

        user_prompt = f"""Here are the user's emails from the past period:

<emails>
{email_content}
</emails>

User's question: {question}

Please analyze the emails and provide a helpful response."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text

    def _format_emails_for_prompt(
        self,
        emails: list[Email],
        include_full_body: bool,
    ) -> str:
        """Format emails for inclusion in prompt."""
        # Sort by date (newest first)
        sorted_emails = sorted(emails, key=lambda e: e.date, reverse=True)

        formatted = []
        total_chars = 0
        max_total_chars = 150000  # Leave room for system prompt and response

        for i, email in enumerate(sorted_emails):
            # Determine body length based on settings and remaining space
            if include_full_body:
                max_body = 3000
            else:
                max_body = 500

            email_text = f"--- Email {i + 1} ---\n{email.to_prompt_format(include_body=True, max_body_length=max_body)}\n"

            if total_chars + len(email_text) > max_total_chars:
                formatted.append(f"\n... ({len(sorted_emails) - i} more emails truncated due to length)")
                break

            formatted.append(email_text)
            total_chars += len(email_text)

        return "\n".join(formatted)

    def summarize_emails(self, emails: list[Email]) -> str:
        """Generate a general summary of the emails."""
        return self.analyze(
            emails,
            "Please provide a brief summary of these emails. Group them by category "
            "(e.g., work, personal, newsletters, notifications) and highlight any "
            "important items that might need attention.",
        )
