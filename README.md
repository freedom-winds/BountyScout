# BountyScout

A tool to scout and notify about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔔 Customizable alert formatting
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Send a bounty alert
const opportunities = [
  { title: 'Bug Bounty #1', reward: 1000 },
  { title: 'Bug Bounty #2', reward: 2000 },
  // ... more opportunities
];

await sendBountyAlert(opportunities.length, opportunities);

// Or just format a title
const title = formatBountyAlertTitle(13);
console.log(title); // "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert title with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities (must be non-negative)

**Returns:** (string) Formatted notification title

**Example:**
```javascript
formatBountyAlertTitle(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyAlertTitle(13); // "🎯 Bounty Alert: 13 New Opportunities found"
```

### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects (optional)

**Returns:** (Promise<Object>) Notification details including title, count, and opportunities

## Fix Details

This fix addresses the typo in the notification title where "Opportunityies" was misspelled. The solution includes:

1. **Proper pluralization logic**: Correctly handles singular "Opportunity" vs plural "Opportunities"
2. **Input validation**: Ensures count is a valid non-negative number
3. **Error handling**: Gracefully handles edge cases and invalid inputs
4. **Comprehensive tests**: Full test coverage for all scenarios
5. **Modular design**: Separated formatting logic from notification service

## License

MIT
