# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Customizable notifications
- 🔍 Advanced filtering and search
- 📊 Analytics and reporting

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Format a notification message
const message = formatBountyNotification(15);
console.log(message); // 🎯 Bounty Alert: 15 New Opportunities found

// Send a notification
await sendBountyNotification(15, opportunities);
```

## Testing

```bash
npm test
```

## API Reference

### `formatBountyNotification(count)`

Formats a notification message with proper grammar.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification message

**Example:**
```javascript
formatBountyNotification(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyNotification(15); // "🎯 Bounty Alert: 15 New Opportunities found"
```

### `sendBountyNotification(count, opportunities)`

Sends a notification about new bounty opportunities.

**Parameters:**
- `count` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects

**Returns:** (Promise<Object>) Notification result

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
