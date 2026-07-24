# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity scanning
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar in notifications
- 🔧 Configurable notification preferences

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
    webhookUrl: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
  },
  discord: {
    webhookUrl: 'https://discord.com/api/webhooks/YOUR/WEBHOOK'
  },
  email: {
    to: 'user@example.com'
  }
});
```

## Testing

```bash
npm test
```

## Configuration

Create a `.env` file with your notification preferences:

```
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
EMAIL_RECIPIENT=your_email@example.com
```

## Grammar Fix

This update fixes the typo "Opportunityies" → "Opportunities" and ensures proper singular/plural grammar:

- 1 opportunity: "1 New Opportunity was found"
- Multiple opportunities: "12 New Opportunities were found"

## License

MIT
