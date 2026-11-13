# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar handling for singular/plural opportunities
- 🔔 Real-time alerts

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

// Send notifications
await sendBountyNotification(12, {
  slack: {
    webhookUrl: process.env.SLACK_WEBHOOK_URL,
    username: 'BountyScout',
    icon: ':dart:'
  },
  discord: {
    webhookUrl: process.env.DISCORD_WEBHOOK_URL
  },
  email: {
    to: 'user@example.com'
  }
});
```

## Configuration

Set the following environment variables:

```bash
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

## Testing

```bash
npm test
```

## Grammar Fix

This update fixes the typo "Opportunityies" → "Opportunities" and ensures proper singular/plural handling:

- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 12 New Opportunities found"

## License

MIT
