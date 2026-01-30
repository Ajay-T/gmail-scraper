# Gmail Scraper

AI-powered Gmail analyzer - scrape and summarize your inbox with natural language queries.

Ask questions like:
- "What jobs have I applied to and been rejected from?"
- "List all receipts from the past month"
- "Summarize my newsletter subscriptions"

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the JSON file and save as `credentials.json` in this directory

### 3. Set up Anthropic API key

Get an API key from [Anthropic Console](https://console.anthropic.com/) and set it:

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. First run (authentication)

On first run, a browser window will open asking you to authorize the app to read your Gmail. This creates a `token.json` file for future use.

## Usage

```bash
# Ask a question about your emails
python main.py "What jobs have I applied to and been rejected from?"

# Look back further (default is 60 days)
python main.py "List all receipts" --days 90

# Filter with Gmail search syntax
python main.py "Summarize these" --query "from:linkedin.com"

# Get a general inbox summary
python main.py --summary

# Include full email bodies (uses more tokens but more accurate)
python main.py "Find shipping notifications" --full-body
```

## Options

| Option | Description |
|--------|-------------|
| `--days N` | Number of days to look back (default: 60) |
| `--max-emails N` | Maximum emails to fetch (default: 500) |
| `--query "..."` | Gmail search query to filter emails |
| `--full-body` | Include full email bodies in analysis |
| `--summary` | Generate a general inbox summary |
| `--credentials PATH` | Path to Google OAuth credentials file |

## Privacy

- **Local processing**: Your emails are fetched locally and sent to Claude's API for analysis
- **Read-only access**: The app only requests read access to your Gmail
- **No storage**: Emails are not stored permanently; they're only held in memory during analysis
- **Credentials stay local**: Your `credentials.json` and `token.json` are gitignored

## License

MIT
