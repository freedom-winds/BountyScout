# BountyScout

Automated bounty opportunity tracker and notification system.

## Features

- 🎯 Automated bounty opportunity discovery
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper grammar and formatting in notifications
- 🔄 Real-time monitoring

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the root directory:

```env
# Slack Configuration
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Discord Configuration
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# Email Configuration
EMAIL_ENABLED=false
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Send notification for new opportunities
const opportunities = [
  { title: 'Bug Bounty #1', url: 'https://example.com/bounty1' },
  { title: 'Bug Bounty #2', url: 'https://example.com/bounty2' }
];

await sendBountyNotification(opportunities.length, opportunities);

// Or just format a message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were found"
```

## Testing

```bash
npm test
```

## Grammar Rules

The notification formatter ensures proper grammar:

- **Singular**: "1 New Opportunity was found"
- **Plural**: "2+ New Opportunities were found"
- **Spelling**: "Opportunities" (not "Opportunityies")

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
