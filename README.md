# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity scanning
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar handling for singular/plural opportunities
- 🔔 Real-time alerts for new bounties

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatOpportunityNotification(12);
console.log(message); // "🎯 Bounty Alert: 12 New Opportunities were found"

// Send notifications
await sendBountyNotification(12, {
  slack: {
    webhookUrl: process.env.SLACK_WEBHOOK_URL,
    username: 'BountyScout',
    icon: ':dart:'
  },
  discord: {
    webhookUrl: process.env.DISCORD_WEBHOOK_URL
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

The notification formatter ensures proper grammar:

- 1 opportunity: "1 New Opportunity was found"
- Multiple opportunities: "12 New Opportunities were found"
- Zero opportunities: "0 New Opportunities were found"

## License

MIT
