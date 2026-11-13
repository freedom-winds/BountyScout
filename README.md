# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notifications with proper grammar
- 🔍 Automated scanning for new opportunities

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatOpportunityNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were found"

// Send a notification
await sendBountyNotification(15, opportunities);
```

## Testing

```bash
npm test
```

## Grammar Rules

The notification system automatically handles proper grammar:
- Single opportunity: "1 New Opportunity was found"
- Multiple opportunities: "15 New Opportunities were found"
- Zero opportunities: "0 New Opportunities were found"

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
