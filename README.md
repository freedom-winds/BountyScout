# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🔍 Automatically scans for new bounty opportunities
- 🎯 Smart notifications with proper grammar
- 📊 Tracks and reports findings
- 🔔 Multiple notification channels (Slack, Discord, Email)

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/notifications/notifier');
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

// Send notification for new opportunities
sendBountyNotification(12, {
  slack: { webhookUrl: 'your-slack-webhook' },
  discord: { webhookUrl: 'your-discord-webhook' }
});

// Format message manually
const message = formatOpportunityMessage(1);
console.log(message); // "🎯 Bounty Alert: 1 New Opportunity found"
```

## Testing

```bash
npm test
```

## Fix: Grammar Correction

This update fixes the typo "Opportunityies" to properly use singular/plural forms:
- 1 opportunity: "1 New Opportunity found"
- Multiple opportunities: "12 New Opportunities found"

The notification formatter now correctly handles singular and plural forms based on the count.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
