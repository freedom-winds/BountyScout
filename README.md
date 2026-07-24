# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🔍 Scans multiple platforms for new bounty opportunities
- 🎯 Smart notifications with proper grammar
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ⚡ Real-time alerts for new opportunities

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the root directory:

```env
# Slack Integration (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord Integration (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL

# Email Integration (optional)
EMAIL_ENABLED=false
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-password
EMAIL_TO=recipient@example.com
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');

// Send notification for new opportunities
const opportunities = [
  {
    title: 'Bug Bounty Program',
    url: 'https://example.com/bounty/1',
    description: 'Find security vulnerabilities',
    reward: '$500-$5000',
    platform: 'HackerOne'
  }
];

await sendBountyNotification(12, opportunities);
```

## Testing

```bash
npm test
```

## Notification Format

The system automatically formats notifications with proper grammar:

- **Singular**: "🎯 Bounty Alert: 1 New Opportunity was found"
- **Plural**: "🎯 Bounty Alert: 12 New Opportunities were found"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
