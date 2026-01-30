"""Tests for email models."""

from datetime import datetime

from src.models.email import Email


def test_email_to_prompt_format():
    """Test email formatting for LLM prompts."""
    email = Email(
        id="123",
        thread_id="456",
        subject="Test Subject",
        sender="sender@example.com",
        recipient="recipient@example.com",
        date=datetime(2024, 1, 15, 10, 30),
        body="This is the email body content.",
        snippet="This is the email...",
        labels=["INBOX"],
    )

    formatted = email.to_prompt_format()

    assert "From: sender@example.com" in formatted
    assert "To: recipient@example.com" in formatted
    assert "Subject: Test Subject" in formatted
    assert "2024-01-15" in formatted
    assert "This is the email body content." in formatted


def test_email_to_prompt_format_truncation():
    """Test that long bodies are truncated."""
    long_body = "x" * 3000
    email = Email(
        id="123",
        thread_id="456",
        subject="Test",
        sender="a@b.com",
        recipient="c@d.com",
        date=datetime.now(),
        body=long_body,
        snippet="",
    )

    formatted = email.to_prompt_format(max_body_length=100)

    assert "[truncated]" in formatted
    assert len(formatted) < len(long_body)


def test_email_str():
    """Test email string representation."""
    email = Email(
        id="123",
        thread_id="456",
        subject="Important Email",
        sender="boss@company.com",
        recipient="me@example.com",
        date=datetime(2024, 6, 20),
        body="Content",
        snippet="",
    )

    assert "2024-06-20" in str(email)
    assert "boss@company.com" in str(email)
    assert "Important Email" in str(email)
