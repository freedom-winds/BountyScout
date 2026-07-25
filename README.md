# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Real-time bounty opportunity detection
- 📧 Smart notifications with proper grammar
- 🔍 Multi-platform scanning
- ⚡ Fast and efficient processing

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');

// Send notification for new opportunities
sendBountyNotification(15);
// Output: 🎯 Bounty Alert: 15 New Opportunities found
```

## Testing

```bash
npm test
```

## Recent Fixes

- ✅ Fixed typo: "Opportunityies" → "Opportunities"
- ✅ Added proper singular/plural handling
- ✅ Improved notification formatting
- ✅ Added comprehensive error handling
- ✅ Added unit tests for notification formatting

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
