# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📬 Smart notifications with proper grammar
- 🔔 Multi-channel alert support
- 📊 Opportunity tracking

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

// Send alert for new opportunities
const opportunities = [
  { id: 1, title: 'Bug Fix', reward: 100 },
  { id: 2, title: 'Feature Request', reward: 200 },
  { id: 3, title: 'Security Issue', reward: 500 }
];

await sendBountyAlert(opportunities);
// Output: 🎯 Bounty Alert: 3 New Opportunities found
```

## Notification Format

The notification system automatically handles singular/plural grammar:

- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 3 New Opportunities found"

## Testing

```bash
npm test
```

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
