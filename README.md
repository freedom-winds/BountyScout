# BountyScout

Automated GitHub bounty and opportunity scanner.

## Features

- Scans GitHub for bounty opportunities every 6 hours
- Searches across multiple keywords: bounties, rewards, good first issues
- Automatically creates issues with findings
- Auto-closes scan results older than 14 days

## How It Works

The scanner runs via GitHub Actions and searches for:
- Bug bounties
- Security bounties
- Hackathon prizes
- Good first issues
- Help wanted issues

Results are posted as issues in this repository with the `bounty-scan` label.

## Manual Trigger

You can manually trigger a scan from the Actions tab:
1. Go to Actions
2. Select "Bounty Scan" workflow
3. Click "Run workflow"

## Configuration

The scan runs automatically every 6 hours. To adjust:
- Edit `.github/workflows/bounty-scan.yml`
- Modify the `cron` schedule

## Labels

All automated issues are tagged with:
- `bounty-scan` - Identifies automated scan results
- `automated` - Marks as bot-generated content

## Cleanup

Old scan issues (>14 days) are automatically closed weekly to keep the repository clean.
