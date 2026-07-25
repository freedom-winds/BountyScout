# BountyScout

A tool for tracking and alerting on new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Multi-channel notifications
- 🔍 Smart filtering and matching
- 📊 Analytics and reporting

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(3);
console.log(message); // "🎯 Bounty Alert: 3 New Opportunities found"

// Send a bounty alert
await sendBountyAlert(3, {
  channels: [emailChannel, slackChannel]
});
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

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
