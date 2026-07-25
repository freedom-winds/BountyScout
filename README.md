# BountyScout

Automated bounty opportunity detection and notification system.

## Features

- 🎯 Automated bounty opportunity detection
- 📧 Smart notification formatting
- 🔔 Configurable alert system
- ✅ Proper pluralization (Opportunity vs Opportunities)

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Format a notification title
const title = formatBountyAlertTitle(3);
console.log(title); // 🎯 Bounty Alert: 3 New Opportunities found

// Send a bounty alert
const opportunities = [
  { id: 1, title: 'Bug Bounty 1', reward: '$500' },
  { id: 2, title: 'Bug Bounty 2', reward: '$1000' },
  { id: 3, title: 'Bug Bounty 3', reward: '$750' }
];

await sendBountyAlert(opportunities, {
  channel: 'slack',
  priority: 'high'
});
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert title with proper pluralization.

- **Parameters:**
  - `count` (number): Number of opportunities found
- **Returns:** (string) Formatted notification title
- **Throws:** Error if count is not a non-negative number

### `sendBountyAlert(opportunities, notificationConfig)`

Sends a bounty alert notification.

- **Parameters:**
  - `opportunities` (Array): Array of opportunity objects
  - `notificationConfig` (Object, optional): Additional notification configuration
- **Returns:** (Promise<Object>) Notification object with title, opportunities, and timestamp
- **Throws:** Error if opportunities is not an array

## License

MIT
