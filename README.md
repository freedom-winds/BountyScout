# BountyScout 🎯

Automated bounty opportunity finder and notification system.

## Features

- 🔍 Automatically scans for new bounty opportunities
- 📢 Sends notifications via Slack, Discord, or Email
- ✅ Proper grammar in notifications (singular/plural handling)
- 🚀 Easy to configure and deploy

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
      "enabled": true,
      "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    },
    "discord": {
      "enabled": true,
      "webhookUrl": "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
    },
    "email": {
      "enabled": false
    }
  }
}
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const config = require('./config.json');

const opportunities = [
  {
    title: 'Bug Bounty Program',
    url: 'https://example.com/bounty',
    description: 'Find security vulnerabilities',
    reward: '$500-$5000',
    platform: 'HackerOne'
  }
];

await sendBountyNotification(opportunities, config.notifications);
```

## Testing

```bash
npm test
```

## Notification Format

The system uses proper grammar for notifications:
- 0 opportunities: "🎯 Bounty Alert: No new opportunities found"
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found" (singular)
- 2+ opportunities: "🎯 Bounty Alert: X New Opportunities found" (plural)

## License

MIT
