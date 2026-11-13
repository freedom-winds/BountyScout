# BountyScout

Automated bug bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity discovery
- 📬 Multi-channel notifications (Slack, Discord, Email)
- 🔍 Customizable search filters
- 📊 Opportunity tracking and analytics

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the root directory:

```env
# Notification Channels (comma-separated: slack,discord,email,console)
NOTIFICATION_CHANNELS=console,slack

# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord Configuration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL

# Email Configuration (if using email notifications)
EMAIL_SERVICE=gmail
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=recipient@example.com
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

// Example: Send notification for new opportunities
const opportunities = [
  {
    title: 'XSS Vulnerability in Web App',
    reward: '$500',
    platform: 'HackerOne'
  },
  {
    title: 'SQL Injection in API',
    reward: '$1000',
    platform: 'Bugcrowd'
  },
  {
    title: 'CSRF in Authentication Flow',
    reward: '$750',
    platform: 'Synack'
  }
];

await sendBountyAlert(opportunities);
```

## Notification Format

Notifications are automatically formatted with proper grammar:
- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 3 New Opportunities found"

## Testing

```bash
npm test
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
