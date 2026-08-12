# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Real-time bounty opportunity detection
- 📧 Smart notification system with proper grammar
- 🔍 Customizable search filters
- 📊 Opportunity tracking and analytics

## Installation

```bash
npm install
```

## Usage

```javascript
const NotificationService = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Create notification service
const notificationService = new NotificationService();

// Send bounty alert
const opportunities = [
  { id: 1, title: 'Fix authentication bug', reward: 500 },
  { id: 2, title: 'Add dark mode', reward: 300 }
];

await notificationService.sendBountyAlert(opportunities.length, opportunities);

// Format notification title
const title = formatBountyAlertTitle(13);
console.log(title); // "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert notification title with proper singular/plural grammar.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification title

**Example:**
```javascript
formatBountyAlertTitle(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyAlertTitle(13); // "🎯 Bounty Alert: 13 New Opportunities found"
```

### `NotificationService.sendBountyAlert(count, opportunities)`

Sends a bounty alert notification.

**Parameters:**
- `count` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects

**Returns:** (Object) Notification result with success status

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
