# Bounty Scanner

Automated GitHub bounty opportunity scanner that searches for bug bounties, CVEs, and other bounty-related issues across GitHub.

## Features

- 🔍 Automated scanning every 6 hours
- 🎯 Searches for bounty opportunities, CVEs, and security issues
- 📊 Updates a single tracking issue with latest results
- 🧹 Automatic cleanup of stale scan reports
- ⚡ Manual trigger support via workflow dispatch

## How It Works

The scanner runs on a schedule and searches GitHub for issues containing bounty-related keywords. Results are posted to a tracking issue labeled `bounty-scan` that gets updated with each scan.

## Workflows

### Bounty Scanner
- **Schedule**: Every 6 hours
- **Trigger**: Manual via Actions tab
- **Output**: Creates or updates bounty scan tracking issue

### Cleanup
- **Schedule**: Weekly on Sundays
- **Trigger**: Manual via Actions tab
- **Action**: Closes bounty scan issues older than 7 days

## Setup

1. Fork or clone this repository
2. Enable GitHub Actions in repository settings
3. The workflows will run automatically on schedule
4. View results in the Issues tab

## Manual Trigger

1. Go to the Actions tab
2. Select "Bounty Scanner" workflow
3. Click "Run workflow"
4. Select branch and run

## Configuration

Edit `.github/workflows/bounty-scan.yml` to customize:
- Search query keywords
- Scan frequency (cron schedule)
- Number of results to display
- Time window for results

## Labels

- `bounty-scan`: Applied to all scan result issues
- `automated`: Indicates automated issue creation

## License

MIT
