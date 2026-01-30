# Next Steps - Gmail Scraper

## Current Status (January 30, 2026)

### What's Built
- [x] Project structure and GitHub repo
- [x] Gmail OAuth2 authentication flow (`src/gmail/auth.py`)
- [x] Gmail API client to fetch emails by date range (`src/gmail/client.py`)
- [x] Email data model with prompt formatting (`src/models/email.py`)
- [x] Claude integration for email analysis (`src/analyzer/llm.py`)
- [x] CLI interface with rich terminal output (`main.py`)
- [x] Basic test structure

### What's NOT Done Yet
- [ ] Google Cloud project setup (requires manual steps)
- [ ] Testing with real Gmail account
- [ ] No caching of fetched emails (re-fetches every time)
- [ ] No interactive mode (single question per run)

---

## Immediate Next Steps (Before First Use)

### 1. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project called "Gmail Scraper" (or similar)
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search "Gmail API" and click Enable
4. Configure OAuth consent screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in app name, support email
   - Add scope: `https://www.googleapis.com/auth/gmail.readonly`
   - Add your email as a test user
5. Create OAuth credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Download JSON and save as `credentials.json` in project root

### 2. Set Up Anthropic API Key

1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Add your key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### 3. Install Dependencies

```bash
cd /Users/ajaytadinada/Personal_Projects/gmail-scraper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. First Test Run

```bash
python main.py --summary --days 7
```

This will:
- Open browser for Gmail authorization (first time only)
- Fetch last 7 days of emails
- Generate a summary

---

## Short-Term Enhancements

### Caching Layer
**Why**: Currently re-fetches all emails every run, which is slow and wasteful.

```
- Add SQLite or JSON cache for fetched emails
- Only fetch new emails since last run
- Add --refresh flag to force re-fetch
```

### Interactive Mode
**Why**: Currently requires a new command for each question.

```
- Add --interactive flag for REPL-style Q&A
- Fetch emails once, then answer multiple questions
- Saves time and API costs
```

### Better Error Handling
```
- Handle rate limits from Gmail API
- Handle Claude API errors gracefully
- Add retry logic
```

### Progress Indicators
```
- Show progress bar when fetching many emails
- Show token count before sending to Claude
- Estimate API cost
```

---

## Future Enhancements (For Multi-User)

### User Authentication System
```
- Web interface with login
- Store OAuth tokens per user (encrypted)
- Multi-account support
```

### Web UI
```
- Flask/FastAPI backend
- React or simple HTML frontend
- Real-time streaming of Claude responses
```

### Preset Queries
```
- "Job search tracker" - applications, responses, interviews
- "Finance summary" - receipts, bills, subscriptions
- "Newsletter digest" - summarize all newsletters
- Custom saved queries
```

### Email Categorization
```
- Auto-categorize emails before analysis
- Filter by category in queries
- Show category breakdown
```

### Export Options
```
- Export results to CSV/JSON
- Generate PDF reports
- Email summary to self
```

### Scheduling
```
- Daily/weekly automated summaries
- Email digest of important items
- Cron job or cloud function
```

---

## Technical Debt / Improvements

- [ ] Add comprehensive test coverage
- [ ] Add type hints everywhere (currently partial)
- [ ] Add logging instead of print statements
- [ ] Consider async for faster email fetching
- [ ] Add rate limiting for API calls
- [ ] Support for attachments (currently ignored)
- [ ] Handle non-UTF8 email encodings better

---

## File Reference

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point, argument parsing |
| `src/gmail/auth.py` | OAuth2 flow, token management |
| `src/gmail/client.py` | Gmail API calls, email parsing |
| `src/models/email.py` | Email dataclass, formatting |
| `src/analyzer/llm.py` | Claude API integration |
| `credentials.json` | Google OAuth credentials (gitignored, you create) |
| `token.json` | Stored auth token (gitignored, auto-created) |
| `.env` | API keys (gitignored, you create) |
