# BountyScout 🎯

Automated bounty opportunity scanner and notification system.

## Features

- 🔍 Scans multiple platforms for new bounty opportunities
- 🔔 Sends notifications via Slack, Discord, and Email
- ✅ Proper grammar handling for singular/plural notifications
- 🚀 Easy to configure and deploy

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file with your notification settings:

```env
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
EMAIL_CONFIG=your_email_config
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

// Format a message
const message = formatOpportunityMessage(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities found"

// Send notification
await sendBountyNotification(15, {
  slack: true,
  slackWebhook: process.env.SLACK_WEBHOOK_URL,
  discord: true,
  discordWebhook: process.env.DISCORD_WEBHOOK_URL
});
```

## Notification Format

The notification system automatically handles proper grammar:

- 0 opportunities: "🎯 Bounty Alert: No new opportunities found"
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found" (singular)
- 2+ opportunities: "🎯 Bounty Alert: 15 New Opportunities found" (plural)

## Testing

```bash
npm test
```

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
