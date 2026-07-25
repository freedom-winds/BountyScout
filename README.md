# BountyScout

A tool for tracking and alerting on new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notification system with proper grammar
- 🔍 Automated opportunity discovery

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Send a bounty alert
await sendBountyAlert(3, opportunities);

// Format a notification title
const title = formatBountyAlertTitle(1); // "🎯 Bounty Alert: 1 New Opportunity found"
const title2 = formatBountyAlertTitle(3); // "🎯 Bounty Alert: 3 New Opportunities found"
```

## Testing

```bash
npm test
```

## Notification Format

The notification system automatically handles singular/plural grammar:

- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 3 New Opportunities found"

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
