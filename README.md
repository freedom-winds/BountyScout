# BountyScout 🎯

Automated bounty opportunity finder and notification system.

## Features

- 🔍 Automatically scans for new bounty opportunities
- 📢 Sends notifications via Slack, Discord, or Email
- ✅ Proper grammar handling (singular/plural)
- 🚀 Production-ready with error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const { checkAndNotify } = require('./src/index');

// Example: Check for opportunities and send notification
const opportunities = [
  { id: 1, title: 'Bug Bounty #1', reward: 500 },
  { id: 2, title: 'Bug Bounty #2', reward: 1000 }
];

const config = {
  slack: true,
  slackWebhook: process.env.SLACK_WEBHOOK_URL,
  discord: false,
  email: false
};

await checkAndNotify(opportunities, config);
// Output: "🎯 Bounty Alert: 2 New Opportunities found"
```

## Configuration

Set up your notification channels:

```javascript
const config = {
  // Slack
  slack: true,
  slackWebhook: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
  
  // Discord
  discord: true,
  discordWebhook: 'https://discord.com/api/webhooks/YOUR/WEBHOOK',
  
  // Email
  email: false,
  emailConfig: {
    from: 'bounty@example.com',
    to: 'you@example.com'
  },
  
  // Other options
  notifyOnZero: false // Set to true to get notifications even when no opportunities found
};
```

## Notification Format

The system uses proper grammar:

- 0 opportunities: "🎯 Bounty Alert: No new opportunities found"
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found" (singular)
- 2+ opportunities: "🎯 Bounty Alert: 13 New Opportunities found" (plural)

## Testing

```bash
npm test
```

## Environment Variables

```bash
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

## License

MIT
