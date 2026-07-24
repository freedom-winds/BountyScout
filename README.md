# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📢 Smart notifications with proper pluralization
- 🔔 Multi-channel alert support (Discord, Slack, Email)
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
  { title: 'Bug Bounty #1', reward: '$500' },
  { title: 'Bug Bounty #2', reward: '$1000' }
];

await sendBountyAlert(opportunities.length, opportunities);

// Format a notification title
const title = formatBountyAlertTitle(12);
console.log(title); // 🎯 Bounty Alert: 12 New Opportunities found
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert notification title with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification title

**Example:**
```javascript
formatBountyAlertTitle(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyAlertTitle(12); // "🎯 Bounty Alert: 12 New Opportunities found"
```

### `sendBountyAlert(opportunityCount, opportunities)`

Sends bounty alert notifications through configured channels.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects (optional)

**Returns:** (Promise) Notification result object

## Contributing

Pull requests are welcome! Please ensure all tests pass before submitting.

## License

MIT
