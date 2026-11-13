# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📢 Smart notifications with proper grammar
- 🔧 Extensible notification handlers
- ✅ Comprehensive error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const { processBounties, notificationService } = require('./src/index');

// Register custom notification handler
notificationService.registerHandler((notification) => {
  // Send to Slack, Discord, email, etc.
  console.log(notification.message);
});

// Process new bounties
const opportunities = [
  { title: 'Bug Bounty 1', url: 'https://...', platform: 'HackerOne', reward: '$500' },
  { title: 'Bug Bounty 2', url: 'https://...', platform: 'Bugcrowd', reward: '$1000' }
];

await processBounties(opportunities);
```

## Notification Format

The system automatically formats notifications with proper grammar:

- 0 opportunities: "🎯 Bounty Alert: No new opportunities found"
- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 12 New Opportunities found"

## Testing

```bash
npm test
```

## API

### `formatBountyNotification(count)`

Formats a bounty notification message with proper grammar.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification message

### `NotificationService`

Service for managing and sending notifications.

**Methods:**
- `registerHandler(handler)`: Register a notification handler function
- `sendBountyAlert(count, metadata)`: Send a bounty alert notification

### `processBounties(opportunities)`

Process and notify about new bounty opportunities.

**Parameters:**
- `opportunities` (Array): Array of opportunity objects

**Returns:** Promise<Object> Result with success status and message

## License

MIT
