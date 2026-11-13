# BountyScout 🎯

Automated bounty opportunity scanner and notification system.

## Features

- Scans for new bounty opportunities
- Sends notifications via multiple channels (Slack, Discord, Email)
- Proper grammar handling for singular/plural opportunities
- Configurable notification preferences

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

// Format a message
const message = formatOpportunityMessage(12);
console.log(message); // "🎯 Bounty Alert: 12 New Opportunities found"

// Send notification
await sendBountyNotification(12, {
  slack: {
    webhookUrl: process.env.SLACK_WEBHOOK_URL,
    username: 'BountyScout',
    icon: ':dart:'
  },
  discord: {
    webhookUrl: process.env.DISCORD_WEBHOOK_URL,
    username: 'BountyScout'
  },
  email: {
    to: 'user@example.com'
  }
});
```

## Configuration

Set the following environment variables:

- `SLACK_WEBHOOK_URL` - Slack webhook URL for notifications
- `DISCORD_WEBHOOK_URL` - Discord webhook URL for notifications

## Testing

```bash
npm test
```

## Grammar Rules

The notification formatter handles proper grammar:

- 0 opportunities: "No new opportunities found"
- 1 opportunity: "1 New Opportunity found" (singular)
- 2+ opportunities: "X New Opportunities found" (plural)

## License

MIT
