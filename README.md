# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Multi-channel notifications (Console, Slack, Discord, Email)
- 🔍 Customizable search filters
- 📊 Opportunity tracking and analytics

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the root directory:

```env
# Notification Channels (comma-separated)
NOTIFICATION_CHANNELS=console,slack,discord

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
    title: 'Web Application Security Testing',
    reward: '$500-$5000',
    platform: 'HackerOne',
    url: 'https://hackerone.com/example'
  },
  {
    title: 'Mobile App Penetration Testing',
    reward: '$1000-$10000',
    platform: 'Bugcrowd',
    url: 'https://bugcrowd.com/example'
  },
  {
    title: 'API Security Assessment',
    reward: '$750-$7500',
    platform: 'Intigriti',
    url: 'https://intigriti.com/example'
  }
];

await sendBountyAlert(opportunities);
```

## Notification Format

Notifications are automatically formatted with proper grammar:
- **1 opportunity**: "🎯 Bounty Alert: 1 New Opportunity found"
- **Multiple opportunities**: "🎯 Bounty Alert: 3 New Opportunities found"

## Testing

```bash
npm test
```

## API Reference

### `formatBountyAlertTitle(count)`

Formats the notification title with proper singular/plural grammar.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification title

**Throws:** Error if count is not a non-negative number

### `sendBountyAlert(opportunities, options)`

Sends bounty alert notifications through configured channels.

**Parameters:**
- `opportunities` (Array): Array of opportunity objects
- `options` (Object): Optional notification settings

**Returns:** Promise

### `formatNotificationMessage(opportunities)`

Formats the notification message body with opportunity details.

**Parameters:**
- `opportunities` (Array): Array of opportunity objects

**Returns:** (string) Formatted message

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
