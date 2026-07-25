# BountyScout

Automated bounty opportunity tracker and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper pluralization in notifications
- 🛡️ Error handling and validation
- 🧪 Comprehensive test coverage

## Installation

```bash
npm install
```

## Configuration

Set up environment variables:

```bash
# Notification Channels (comma-separated)
NOTIFICATION_CHANNELS=console,slack,discord

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord Configuration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

// Send notification for new opportunities
const opportunities = [
  { title: 'Bug Fix Needed', reward: '$500' },
  { title: 'Feature Request', reward: '$1000' },
  { title: 'Security Audit', reward: '$2000' }
];

await sendBountyAlert(opportunities.length, opportunities);
```

## Notification Format

The system automatically formats notifications with proper grammar:

- **1 opportunity**: "🎯 Bounty Alert: 1 New Opportunity found"
- **Multiple opportunities**: "🎯 Bounty Alert: 3 New Opportunities found"

## Testing

```bash
npm test
```

## Error Handling

The system includes comprehensive error handling:

- Validates opportunity counts
- Handles missing or invalid data
- Gracefully degrades if notification channels fail
- Logs errors for debugging

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass
2. Code follows existing conventions
3. New features include tests
4. Documentation is updated

## License

MIT
