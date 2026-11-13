# BountyScout

A tool for tracking and alerting on new bug bounty opportunities.

## Features

- 🎯 Real-time bounty opportunity tracking
- 📧 Smart notification system with proper grammar
- 🔍 Multi-platform support (HackerOne, Bugcrowd, Intigriti, etc.)
- ⚡ Fast and efficient scanning

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
  { id: 1, title: 'XSS Vulnerability', url: 'https://...', reward: '$500', platform: 'HackerOne' },
  { id: 2, title: 'SQL Injection', url: 'https://...', reward: '$1000', platform: 'Bugcrowd' },
  { id: 3, title: 'CSRF Bug', url: 'https://...', reward: '$750', platform: 'Intigriti' }
];

await sendBountyAlert(3, opportunities);
```

## Testing

```bash
npm test
```

## Fix Details

This fix addresses the typo in bounty alert notifications:
- ❌ Before: "3 New Opportunityies found" (incorrect)
- ✅ After: "3 New Opportunities found" (correct)

The implementation includes:
- Proper singular/plural handling ("Opportunity" vs "Opportunities")
- Comprehensive error handling
- Full test coverage
- Production-ready notification service

## License

MIT
