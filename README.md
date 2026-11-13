# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity discovery
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar and spelling in notifications
- 🔍 Customizable search filters

## Installation

```bash
npm install
```

## Configuration

Set up your environment variables:

```bash
# Notification Channels
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
EMAIL_ENABLED=true
EMAIL_RECIPIENT=your@email.com
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were found"

// Send notifications
await sendBountyNotification(15, opportunities);
```

## Notification Format

The notification system uses proper grammar:
- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity was found"
- Multiple opportunities: "🎯 Bounty Alert: 15 New Opportunities were found"

## Testing

```bash
npm test
```

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. Code follows existing conventions
3. Proper error handling is implemented
4. Documentation is updated

## License

MIT
