# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📢 Smart notifications with proper pluralization
- 🔔 Real-time alerts for new opportunities
- 📊 Opportunity tracking and management

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Send a notification for new opportunities
const opportunities = [
  { id: 1, title: 'Bug Fix', reward: 100 },
  { id: 2, title: 'Feature Request', reward: 200 }
];

await sendBountyAlert(opportunities.length, opportunities);

// Or just format a title
const title = formatBountyAlertTitle(15);
console.log(title); // "🎯 Bounty Alert: 15 New Opportunities found"
```

## Testing

```bash
npm test
```

## API

### `formatBountyAlertTitle(count)`

Formats a bounty alert title with proper pluralization.

**Parameters:**
- `count` (number): Number of opportunities found

**Returns:** (string) Formatted notification title

**Example:**
```javascript
formatBountyAlertTitle(1);  // "🎯 Bounty Alert: 1 New Opportunity found"
formatBountyAlertTitle(15); // "🎯 Bounty Alert: 15 New Opportunities found"
```

### `sendBountyAlert(opportunityCount, opportunities)`

Sends a bounty alert notification.

**Parameters:**
- `opportunityCount` (number): Number of new opportunities
- `opportunities` (Array): Array of opportunity objects (optional)

**Returns:** (Promise<Object>) Notification result with success status

## Bug Fixes

### Fixed: Typo in notification title

**Issue:** The notification title contained "Opportunityies" instead of "Opportunities"

**Solution:** 
- Implemented proper pluralization logic
- Added comprehensive test coverage
- Created reusable notification formatting utilities

## License

MIT
