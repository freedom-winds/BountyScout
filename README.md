# BountyScout

Automated bounty opportunity finder and notifier.

## Features

- 🎯 Automated bounty opportunity detection
- 📢 Smart notifications with proper grammar
- 🔍 Comprehensive opportunity tracking
- ✅ Production-ready error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatOpportunityNotification(12);
console.log(message); // "🎯 Bounty Alert: 12 New Opportunities were found"

// Send a notification
const opportunities = [
  { title: 'Bug Fix', reward: '$500' },
  { title: 'Feature Request', reward: '$1000' }
];

await sendBountyNotification(12, opportunities);
```

## Testing

```bash
npm test
```

## API

### `formatOpportunityNotification(count)`

Formats a notification message with proper grammar.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification message

**Example:**
```javascript
formatOpportunityNotification(1);  // "🎯 Bounty Alert: 1 New Opportunity was found"
formatOpportunityNotification(12); // "🎯 Bounty Alert: 12 New Opportunities were found"
```

### `sendBountyNotification(count, opportunities)`

Sends notifications about new bounty opportunities.

**Parameters:**
- `count` (number): Number of new opportunities found
- `opportunities` (Array, optional): Array of opportunity objects

**Returns:** (Promise<string>) Formatted notification message

## Grammar Rules

The notification formatter ensures proper grammar:
- Singular: "1 New Opportunity was found"
- Plural: "N New Opportunities were found" (where N > 1)
- Zero: "0 New Opportunities were found"

## Error Handling

- Validates input types and ranges
- Throws descriptive errors for invalid inputs
- Gracefully handles notification failures
- Comprehensive error logging

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
