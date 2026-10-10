# BountyScout

Scan GitHub repositories for bounty opportunities.

## Setup

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Fill in your credentials:
   ```bash
   GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   TELEGRAM_CHAT_ID=-1001234567890
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

```bash
python -m src.main
```

Or with automatic scanning:
```bash
python -m src.main --auto
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token | — |
| `BOUNTY_REPOSITORIES` | Comma-separated repo list | (see .env.example) |
| `SCAN_INTERVAL_SECONDS` | Scan frequency | 3600 |
| `DISCORD_WEBHOOK_URL` | Discord webhook for alerts | — |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | — |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | — |

## Output

Results are saved as JSON in `./output/` with timestamped filenames.

## License

MIT
