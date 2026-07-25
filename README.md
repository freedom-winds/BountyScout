# BountyScout

Automated bug bounty opportunity scout and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Multi-channel notifications (Slack, Discord, Email)
- ✅ Proper pluralization in notifications
- 🧪 Comprehensive test coverage

## Installation

```bash
npm install
```

## Configuration

Set up environment variables for notification channels:

```bash
# Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord notifications
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL

# Email notifications
EMAIL_ENABLED=true
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

// Send notification for new opportunities
const opportunities = [
  { title: 'XSS Vulnerability', reward: '$500' },
  { title: 'SQL Injection', reward: '$1000' }
];

await sendBountyAlert(opportunities.length, opportunities);
```

## Notification Format

The system automatically formats notifications with proper grammar:

- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 15 New Opportunities found"

## Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

## API

### `formatBountyAlertTitle(count)`

Formats a notification title with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities (must be non-negative)

**Returns:** (string) Formatted notification title

**Throws:** Error if count is not a non-negative number

### `sendBountyAlert(opportunityCount, opportunities)`

Sends bounty alert notifications through configured channels.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects (optional)

**Returns:** Promise<Object> Notification object

## Error Handling

The system includes comprehensive error handling:

- Input validation for notification counts
- Graceful handling of missing configuration
- Failed notification channel recovery
- Detailed error logging

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
