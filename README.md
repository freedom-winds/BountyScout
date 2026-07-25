# BountyScout 🎯

Automated bug bounty opportunity finder and notifier.

## Features

- 🔍 Automatically scans multiple bug bounty platforms
- 📢 Smart notifications with proper grammar
- 🔔 Multi-channel notifications (Slack, Discord, Email)
- 📊 Tracks and filters new opportunities

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the root directory:

```env
# Notification Channels
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
EMAIL_ENABLED=false

# Scanning Configuration
SCAN_INTERVAL=3600000  # 1 hour in milliseconds
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were Found"

// Send notifications
const opportunities = [
  {
    title: 'XSS Vulnerability',
    url: 'https://example.com/bounty/123',
    description: 'Cross-site scripting vulnerability in login form',
    reward: '$500-$1000',
    platform: 'HackerOne'
  }
];

await sendBountyNotification(15, opportunities);
```

## Testing

```bash
npm test
```

## Notification Format

The notification system uses proper grammar:
- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity was Found"
- Multiple opportunities: "🎯 Bounty Alert: 15 New Opportunities were Found"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
