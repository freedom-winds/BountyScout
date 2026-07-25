# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notifications with proper grammar
- 🔍 Automated opportunity discovery

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

// Send a bounty alert
await notificationService.sendBountyAlert(15, {
  channel: 'slack',
  priority: 'high'
});

// Format notification titles
const title = formatBountyAlertTitle(15);
console.log(title); // "🎯 Bounty Alert: 15 New Opportunities found"
```

## Testing

```bash
npm test
```

## Fix Applied

This fix addresses the typo in the notification title where "Opportunityies" was incorrectly spelled. The solution includes:

1. **Proper pluralization logic**: Correctly handles singular "Opportunity" vs plural "Opportunities"
2. **Utility function**: `formatBountyAlertTitle()` with proper grammar rules
3. **Notification service**: Integrated service for sending bounty alerts
4. **Comprehensive tests**: Full test coverage for edge cases
5. **Error handling**: Validates input and handles errors gracefully

## License

MIT
