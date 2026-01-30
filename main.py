#!/usr/bin/env python3
"""
Gmail Scraper - AI-powered email analysis tool.

Fetch emails from your Gmail account and analyze them using Claude.
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

from src.gmail import GmailAuthenticator, GmailClient
from src.analyzer import EmailAnalyzer

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze your Gmail inbox with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What jobs have I applied to and been rejected from?"
  %(prog)s "Summarize all newsletters from the past month" --days 30
  %(prog)s "List all receipts and purchases" --days 90
  %(prog)s --summary  # Get a general summary of your inbox
        """,
    )

    parser.add_argument(
        "question",
        nargs="?",
        help="Question to ask about your emails",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="Number of days to look back (default: 60)",
    )
    parser.add_argument(
        "--max-emails",
        type=int,
        default=500,
        help="Maximum number of emails to fetch (default: 500)",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Gmail search query to filter emails (e.g., 'from:linkedin.com')",
    )
    parser.add_argument(
        "--full-body",
        action="store_true",
        help="Include full email bodies in analysis (uses more tokens)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Generate a general summary of your inbox",
    )
    parser.add_argument(
        "--credentials",
        type=str,
        default="credentials.json",
        help="Path to Google OAuth credentials file",
    )

    args = parser.parse_args()

    if not args.question and not args.summary:
        parser.error("Please provide a question or use --summary")

    try:
        # Authenticate with Gmail
        console.print("\n[bold blue]Gmail Scraper[/bold blue] - AI-powered email analysis\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Authenticate
            task = progress.add_task("Authenticating with Gmail...", total=None)
            auth = GmailAuthenticator(credentials_path=args.credentials)
            creds = auth.authenticate()
            progress.update(task, description="[green]✓[/green] Authenticated with Gmail")

            # Step 2: Fetch emails
            progress.update(task, description=f"Fetching emails from the past {args.days} days...")
            client = GmailClient(creds)
            emails = client.fetch_emails(
                days_back=args.days,
                max_results=args.max_emails,
                query=args.query,
            )
            progress.update(
                task,
                description=f"[green]✓[/green] Fetched {len(emails)} emails",
            )

            if not emails:
                console.print("[yellow]No emails found matching your criteria.[/yellow]")
                return

            # Step 3: Analyze
            progress.update(task, description="Analyzing emails with Claude...")
            analyzer = EmailAnalyzer()

            if args.summary:
                result = analyzer.summarize_emails(emails)
            else:
                result = analyzer.analyze(
                    emails,
                    args.question,
                    include_full_body=args.full_body,
                )
            progress.update(task, description="[green]✓[/green] Analysis complete")

        # Display result
        console.print()
        console.print(
            Panel(
                result,
                title="[bold]Analysis Result[/bold]",
                border_style="green",
                padding=(1, 2),
            )
        )
        console.print()

    except FileNotFoundError as e:
        console.print(f"\n[red]Error:[/red] {e}")
        sys.exit(1)
    except ValueError as e:
        console.print(f"\n[red]Configuration Error:[/red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise


if __name__ == "__main__":
    main()
