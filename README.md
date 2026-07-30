# BountyScout

Automated GitHub bounty opportunity scanner.

## Features

- Scans GitHub for bounty-labeled issues
- Creates consolidated alerts with new opportunities
- Automatic filtering of self-referential alerts
- Deduplication of bounty alert issues

## Automated Workflows

### Filter Valid Bounties
Automatically closes bounty alert issues that reference this repository, preventing recursive scanning loops.

### Deduplicate Bounty Issues
Runs every 6 hours to close duplicate bounty alert issues, keeping only the most recent one.

## Configuration

The scanner filters out:
- Self-referential bounty alerts (alerts that include this repo)
- Duplicate bounty alert issues
- Invalid or malformed bounty posts

## Manual Actions

To manually trigger deduplication:
1. Go to Actions tab
2. Select "Deduplicate Bounty Issues" workflow
3. Click "Run workflow"

## License

MIT
