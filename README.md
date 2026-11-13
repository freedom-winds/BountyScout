# BountyScout

Automated bug bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty opportunity scanning
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar and formatting in notifications
- 🔔 Real-time alerts for new opportunities

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities found"

// Send notifications
await sendBountyAlert(15, {
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
    to: 'your-email@example.com'
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

## Bug Fixes

### Fixed: Typo in notification message

- ✅ Changed "Opportunityies" to "Opportunities"
- ✅ Added proper singular/plural handling
- ✅ Implemented comprehensive error handling
- ✅ Added unit tests for notification formatting

## License

MIT
