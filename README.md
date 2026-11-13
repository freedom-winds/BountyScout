# BountyScout

A tool for tracking and notifying about new bounty opportunities.

## Features

- Automated bounty opportunity detection
- Smart notifications with proper grammar
- Support for multiple notification channels

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Send notification for new opportunities
await sendBountyNotification(15, opportunities);

// Or just format a message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were found"
```

## Testing

```bash
npm test
```

## Grammar Rules

The notification formatter automatically handles:
- Singular vs plural ("Opportunity" vs "Opportunities")
- Proper verb conjugation ("was" vs "were")
- Correct spelling ("Opportunities" not "Opportunityies")

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
