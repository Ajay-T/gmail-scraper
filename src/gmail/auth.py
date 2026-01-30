"""Gmail OAuth2 authentication handler."""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the token.json file
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailAuthenticator:
    """Handles Gmail OAuth2 authentication flow."""

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
    ):
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)

    def authenticate(self) -> Credentials:
        """
        Authenticate with Gmail API using OAuth2.

        Returns:
            Credentials object for API access.

        Raises:
            FileNotFoundError: If credentials.json is not found.
        """
        creds = None

        # Check for existing token
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        # If no valid credentials, run auth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Download it from Google Cloud Console:\n"
                        "1. Go to https://console.cloud.google.com/apis/credentials\n"
                        "2. Create OAuth 2.0 Client ID (Desktop app)\n"
                        "3. Download JSON and save as 'credentials.json'"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds
