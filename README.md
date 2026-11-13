# BountyScout 🎯

Automated bounty opportunity scanner and notifier.

## Features

- Scans multiple platforms for new bounty opportunities
- Sends notifications via Slack, Discord, and Email
- Proper grammar handling for notification messages
- Configurable notification channels

## Installation

```bash
npm install
```

## Configuration

Set up your environment variables:

```bash
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

## Usage

```javascript
const { scanBounties } = require('./src/index');

async function main() {
  const opportunities = await scanBounties();
  console.log(`Found ${opportunities.length} opportunities`);
}

main();
```

## Notification Format

The notification system uses proper grammar:
- 0 opportunities: "🎯 Bounty Alert: No new opportunities found"
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found" (singular)
- 2+ opportunities: "🎯 Bounty Alert: 12 New Opportunities found" (plural)

## Testing

```bash
npm test
```

## License

MIT
