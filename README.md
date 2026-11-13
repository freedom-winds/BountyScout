# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Multi-channel notifications (Slack, Discord, Email)
- 🔍 Smart filtering and deduplication
- 📊 Opportunity tracking and analytics

## Installation

```bash
npm install
```

## Configuration

Create a `config.json` file:

```json
{
  "notifications": {
    "slack": {
      "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    },
    "discord": {
      "webhookUrl": "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
    },
    "email": {
      "to": "your-email@example.com",
      "from": "noreply@bountyscout.com"
    }
  }
}
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const config = require('./config.json');

const opportunities = [
  {
    title: 'XSS Vulnerability',
    reward: '$500',
    platform: 'HackerOne',
    url: 'https://example.com/bounty/1'
  }
];

await sendBountyAlert(opportunities, config.notifications);
```

## Notification Format

Notifications are automatically formatted with proper grammar:
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 3 New Opportunities found"

## Testing

```bash
npm test
```

## License

MIT
