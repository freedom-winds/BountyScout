# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📢 Smart notification system with proper pluralization
- 🔔 Batch notification support
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

### Basic Notification

```javascript
const NotificationService = require('./src/services/notificationService');

const service = new NotificationService();

// Send a single bounty alert
await service.sendBountyAlert(13);
// Output: 🎯 Bounty Alert: 13 New Opportunities found

// Send alert with options
await service.sendBountyAlert(1, {
  priority: 'high',
  channel: 'slack'
});
// Output: 🎯 Bounty Alert: 1 New Opportunity found
```

### Batch Notifications

```javascript
const counts = [1, 5, 13];
const results = await service.sendBatchBountyAlerts(counts);
```

### Using the Formatter Directly

```javascript
const { formatBountyAlert } = require('./src/utils/notificationFormatter');

const message = formatBountyAlert(13);
console.log(message);
// Output: 🎯 Bounty Alert: 13 New Opportunities found
```

## Testing

```bash
npm test
```

## API Reference

### NotificationService

#### `sendBountyAlert(opportunityCount, options)`

Sends a bounty alert notification.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities found
- `options` (Object, optional): Additional notification options

**Returns:** Promise<Object> with `success` and `notification` or `error`

#### `sendBatchBountyAlerts(counts)`

Sends multiple bounty alerts.

**Parameters:**
- `counts` (Array<number>): Array of opportunity counts

**Returns:** Promise<Array<Object>> with results for each notification

### formatBountyAlert(count)

Formats a bounty alert message with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities

**Returns:** String with formatted message

**Throws:** Error if count is not a non-negative number

## Error Handling

The notification system includes comprehensive error handling:

- Validates input types and ranges
- Gracefully handles invalid counts
- Logs errors for debugging
- Returns structured error responses

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
