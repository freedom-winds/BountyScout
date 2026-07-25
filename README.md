# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🔍 Scans multiple platforms for new bounty opportunities
- 🎯 Smart notifications with proper grammar
- 📊 Tracks and reports findings
- 🔔 Multi-channel notifications (Slack, Discord, Email)

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were found"

// Send notification
await sendBountyNotification(15, opportunities);
```

## Testing

```bash
npm test
```

## Configuration

Set up your notification channels via environment variables:

```bash
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
EMAIL_SERVICE=your_email_service
```

## Grammar Rules

The notification system automatically handles:
- Singular vs plural ("Opportunity" vs "Opportunities")
- Proper verb conjugation ("was" vs "were")
- Correct spelling

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
