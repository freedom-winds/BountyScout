# Bounty Hunter

Automated GitHub bounty opportunity scanner that finds and tracks bug bounty and feature bounty issues across GitHub.

## Features

- 🔍 Automated scanning for bounty opportunities every 6 hours
- 📊 Consolidated reporting in GitHub Issues
- 🔄 Automatic updates to existing alerts
- 🧹 Auto-cleanup of stale alerts after 7 days
- 🏷️ Organized with labels for easy filtering

## How It Works

1. **Scheduled Scans**: The workflow runs every 6 hours searching for issues containing "bounty" or "bug bounty"
2. **Issue Creation**: Creates or updates a bounty alert issue with the latest opportunities
3. **Stale Cleanup**: Automatically closes alerts older than 7 days

## Setup

1. Fork this repository
2. Enable GitHub Actions in your repository settings
3. The scanner will run automatically on schedule
4. Manually trigger via Actions tab → Bounty Scanner → Run workflow

## Customization

Edit `.github/workflows/bounty-scanner.yml` to customize:
- Scan frequency (default: every 6 hours)
- Search query terms
- Number of results displayed
- Alert retention period

## Labels

- `bounty-alert`: Automated bounty opportunity posts
- `automated`: System-generated content

## Manual Trigger

You can manually trigger a scan:
1. Go to the Actions tab
2. Select "Bounty Scanner"
3. Click "Run workflow"

## License

MIT
