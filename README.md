# BountyScout

A tool to scout and track bounty opportunities.

## Features

- Automated bounty opportunity detection
- Real-time notifications with proper grammar
- Customizable alert thresholds

## Usage

```javascript
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

// Format notification messages
const message = formatOpportunityMessage(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities found"
```

## Grammar Fix

The notification system now properly handles singular and plural forms:
- 0 opportunities: "No new opportunities found"
- 1 opportunity: "1 New Opportunity found" (singular)
- 2+ opportunities: "X New Opportunities found" (plural)

## Testing

Run tests with:
```bash
npm test
```

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
