# BountyScout

Automated bounty opportunity detection and notification system.

## Features

- 🎯 Real-time bounty opportunity detection
- 📧 Multi-channel notifications (Email, Slack, Discord, etc.)
- ✅ Proper grammar and formatting in notifications
- 🧪 Comprehensive test coverage
- 🔒 Error handling and resilience

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(12);
console.log(message); // "🎯 Bounty Alert: 12 New Opportunities found"

// Send notification through channels
await sendBountyNotification(12, {
  channels: [
    emailChannel,
    slackChannel
  ]
});
```

## Testing

```bash
npm test
```

## Recent Fixes

### Fixed: Typo in notification messages
- ✅ Changed "Opportunityies" to "Opportunities"
- ✅ Added proper singular/plural handling
- ✅ Implemented comprehensive validation
- ✅ Added unit tests for edge cases

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
