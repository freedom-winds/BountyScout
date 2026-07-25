# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- Scans for new bounty opportunities
- Sends formatted notifications
- Proper grammar handling for singular/plural opportunities

## Installation

```bash
npm install
```

## Usage

```javascript
const { formatBountyNotification } = require('./src/utils/notificationFormatter');
const { sendBountyNotification } = require('./src/services/notificationService');

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

## Bug Fixes

### Fixed: Typo in notification message
- Changed "Opportunityies" to "Opportunities" (correct plural form)
- Added proper singular/plural handling
- Implemented comprehensive error handling

## License

MIT
