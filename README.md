# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Smart notifications with proper grammar
- 🔍 Customizable search criteria
- 📊 Opportunity tracking and reporting

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

// Send notification for new opportunities
await sendBountyNotification(13, opportunities);

// Format a message
const message = formatOpportunityMessage(13);
// Output: "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## Grammar Fix

This update fixes the typo "Opportunityies" to "Opportunities" with proper singular/plural handling:

- 0 opportunities: "No new opportunities found"
- 1 opportunity: "1 New Opportunity found" (singular)
- 2+ opportunities: "X New Opportunities found" (plural)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
