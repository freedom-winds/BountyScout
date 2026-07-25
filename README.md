# BountyScout

A tool for tracking and alerting on new bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📬 Smart notifications with proper grammar
- 🔍 Automated bounty discovery

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Format notification titles
const title = formatBountyAlertTitle(3);
// Returns: "🎯 Bounty Alert: 3 New Opportunities found"

// Send notifications
const opportunities = [
  { id: 1, title: 'Bug Bounty', reward: 500 },
  { id: 2, title: 'Security Audit', reward: 1000 }
];

await sendBountyAlert(opportunities, notificationClient);
```

## Testing

```bash
npm test
```

## Bug Fixes

### Fixed: Typo in notification title

**Issue:** Notification title showed "Opportunityies" instead of "Opportunities"

**Solution:** 
- Implemented proper singular/plural handling in `formatBountyAlertTitle`
- Added comprehensive test coverage
- Ensured grammatically correct notifications for all cases:
  - 0 opportunities: "No new opportunities found"
  - 1 opportunity: "1 New Opportunity found"
  - 2+ opportunities: "X New Opportunities found"

## License

MIT
