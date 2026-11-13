# Bounty Hunter

Automated bounty opportunity scanner that monitors multiple repositories for open bounties and good first issues.

## Features

- Scans multiple repositories every 6 hours
- Aggregates issues with bounty, good first issue, and help wanted labels
- Creates/updates a single tracking issue with latest opportunities
- Automatically closes outdated scans weekly
- Sorts by most recently updated

## Monitored Repositories

- solanabr/superteam-academy
- Jagadeeshftw/grainlify
- StellarRoute/StellarRoute

## Workflows

### Bounty Scanner
- **Schedule**: Every 6 hours
- **Manual**: Via workflow_dispatch
- **Action**: Scans repos and creates/updates issue #282

### Cleanup
- **Schedule**: Weekly on Sunday
- **Action**: Closes bounty scan issues older than 7 days

## Configuration

To add more repositories, edit `.github/workflows/bounty-scanner.yml` and add to the `repos` array.

## Labels

The scanner looks for issues with these labels:
- `bounty`
- `good first issue`
- `help wanted`

Scanned issues are tagged with:
- `bounty-scan`
- `automated`
