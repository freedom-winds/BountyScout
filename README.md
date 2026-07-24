# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar and spelling in notifications
- 🔔 Real-time alerts for new opportunities

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file with the following variables:

```env
# Slack Integration (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord Integration (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL

# Email Integration (optional)
EMAIL_ENABLED=false
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(12);
console.log(message); // "🎯 Bounty Alert: 12 New Opportunities were found"

// Send notifications
const opportunities = [
  { title: 'Bug Bounty', url: 'https://example.com', description: 'Find bugs' },
  // ... more opportunities
];

await sendBountyNotification(12, opportunities);
```

## Testing

```bash
npm test
```

## Notification Format

The notification system automatically handles proper grammar:

- Single opportunity: "1 New Opportunity was found"
- Multiple opportunities: "12 New Opportunities were found"
- Zero opportunities: "0 New Opportunities were found"

## Contributing

Pull requests are welcome! Please ensure all tests pass before submitting.

## License

MIT
