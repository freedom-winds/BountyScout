# BountyScout 🎯

Automated bounty opportunity scanner and notification system.

## Features

- 🔍 Scans for new bounty opportunities
- 📢 Sends formatted notifications
- ✅ Proper grammar handling (Opportunity vs Opportunities)
- 🛡️ Robust error handling
- 🧪 Comprehensive test coverage

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
  { id: 1, title: 'Bug Fix', reward: 100 },
  { id: 2, title: 'Feature Request', reward: 200 },
  { id: 3, title: 'Security Issue', reward: 500 }
];

await sendBountyAlert(3, opportunities);
// Output: 🎯 Bounty Alert: 3 New Opportunities found

// Format a title
const title = formatBountyAlertTitle(1);
// Output: 🎯 Bounty Alert: 1 New Opportunity found
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert title with proper grammar.

**Parameters:**
- `count` (number): Number of new opportunities

**Returns:** (string) Formatted title

**Examples:**
- `formatBountyAlertTitle(1)` → "🎯 Bounty Alert: 1 New Opportunity found"
- `formatBountyAlertTitle(3)` → "🎯 Bounty Alert: 3 New Opportunities found"
- `formatBountyAlertTitle(0)` → "🎯 Bounty Alert: No new opportunities found"

### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects

**Returns:** (Object) Result object with success status and notification details

## Error Handling

The system includes comprehensive error handling for:
- Invalid input types
- Negative numbers
- Non-array opportunity lists
- Edge cases

## License

MIT
