# BountyScout

A tool for tracking and alerting on new bounty opportunities.

## Features

- 🎯 Real-time bounty alerts with proper grammar
- 📊 Dashboard for viewing opportunities
- 🔔 Customizable notifications

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
console.log(title); // "🎯 Bounty Alert: 3 New Opportunities found"

// Send a bounty alert
const opportunities = [
  { title: 'Bug Fix', reward: '$500' },
  { title: 'Feature Request', reward: '$1000' },
  { title: 'Security Issue', reward: '$2000' }
];

await sendBountyAlert(3, opportunities, notificationClient);
```

## Testing

```bash
npm test
```

## Grammar Fix

This update fixes the typo "Opportunityies" to "Opportunities" (or "Opportunity" for singular cases) in bounty alert notifications. The notification formatter now correctly handles:

- Singular: "1 New Opportunity found"
- Plural: "3 New Opportunities found"

## License

MIT
