"""Gmail API client for fetching and parsing emails."""

import base64
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Optional

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from src.models.email import Email


class GmailClient:
    """Client for interacting with Gmail API."""

    def __init__(self, credentials: Credentials):
        self.service = build("gmail", "v1", credentials=credentials)
        self.user_id = "me"

    def fetch_emails(
        self,
        days_back: int = 60,
        max_results: int = 500,
        query: Optional[str] = None,
    ) -> list[Email]:
        """
        Fetch emails from the past N days.

        Args:
            days_back: Number of days to look back (default 60 = ~2 months)
            max_results: Maximum number of emails to fetch
            query: Optional Gmail search query to filter emails

        Returns:
            List of Email objects
        """
        # Build date query
        after_date = datetime.now() - timedelta(days=days_back)
        date_query = f"after:{after_date.strftime('%Y/%m/%d')}"

        full_query = date_query
        if query:
            full_query = f"{date_query} {query}"

        # Fetch message IDs
        messages = []
        page_token = None

        while len(messages) < max_results:
            result = (
                self.service.users()
                .messages()
                .list(
                    userId=self.user_id,
                    q=full_query,
                    maxResults=min(100, max_results - len(messages)),
                    pageToken=page_token,
                )
                .execute()
            )

            if "messages" in result:
                messages.extend(result["messages"])

            page_token = result.get("nextPageToken")
            if not page_token:
                break

        # Fetch full message details
        emails = []
        for msg in messages:
            email = self._get_email_details(msg["id"])
            if email:
                emails.append(email)

        return emails

    def _get_email_details(self, message_id: str) -> Optional[Email]:
        """Fetch and parse a single email by ID."""
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId=self.user_id, id=message_id, format="full")
                .execute()
            )

            headers = {h["name"]: h["value"] for h in message["payload"]["headers"]}

            # Parse date
            date_str = headers.get("Date", "")
            try:
                date = parsedate_to_datetime(date_str)
            except (ValueError, TypeError):
                date = datetime.now()

            # Extract body
            body = self._extract_body(message["payload"])

            return Email(
                id=message_id,
                thread_id=message.get("threadId", ""),
                subject=headers.get("Subject", "(No Subject)"),
                sender=headers.get("From", ""),
                recipient=headers.get("To", ""),
                date=date,
                body=body,
                snippet=message.get("snippet", ""),
                labels=message.get("labelIds", []),
            )

        except Exception as e:
            print(f"Error fetching email {message_id}: {e}")
            return None

    def _extract_body(self, payload: dict) -> str:
        """Extract plain text body from email payload."""
        body = ""

        if "body" in payload and payload["body"].get("data"):
            body = self._decode_base64(payload["body"]["data"])
        elif "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    if "body" in part and part["body"].get("data"):
                        body = self._decode_base64(part["body"]["data"])
                        break
                elif part.get("mimeType") == "text/html" and not body:
                    # Fallback to HTML if no plain text
                    if "body" in part and part["body"].get("data"):
                        body = self._decode_base64(part["body"]["data"])
                        body = self._strip_html(body)
                elif "parts" in part:
                    # Handle nested multipart
                    body = self._extract_body(part)
                    if body:
                        break

        return body.strip()

    def _decode_base64(self, data: str) -> str:
        """Decode base64url encoded string."""
        try:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        except Exception:
            return ""

    def _strip_html(self, html: str) -> str:
        """Remove HTML tags and decode entities."""
        # Remove script and style elements
        html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", html)
        # Decode common HTML entities
        text = text.replace("&nbsp;", " ")
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)
        return text.strip()
