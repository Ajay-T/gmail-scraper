"""Email data models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Email:
    """Represents a parsed email message."""

    id: str
    thread_id: str
    subject: str
    sender: str
    recipient: str
    date: datetime
    body: str
    snippet: str = ""
    labels: list[str] = field(default_factory=list)

    def to_prompt_format(self, include_body: bool = True, max_body_length: int = 2000) -> str:
        """
        Format email for inclusion in LLM prompt.

        Args:
            include_body: Whether to include the full body
            max_body_length: Maximum characters to include from body

        Returns:
            Formatted string representation
        """
        lines = [
            f"From: {self.sender}",
            f"To: {self.recipient}",
            f"Date: {self.date.strftime('%Y-%m-%d %H:%M')}",
            f"Subject: {self.subject}",
        ]

        if include_body:
            body = self.body[:max_body_length]
            if len(self.body) > max_body_length:
                body += "... [truncated]"
            lines.append(f"Body:\n{body}")
        else:
            lines.append(f"Preview: {self.snippet}")

        return "\n".join(lines)

    def __str__(self) -> str:
        return f"[{self.date.strftime('%Y-%m-%d')}] {self.sender}: {self.subject}"
