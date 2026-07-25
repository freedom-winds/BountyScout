# BountyScout

Automated bounty opportunity scanner and notification system.

## Features

- 🎯 Automated bounty scanning
- 📢 Smart notifications with proper grammar
- 🔍 Opportunity tracking
- ✅ Production-ready error handling

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

// Send a notification
await sendBountyNotification(15, opportunities);

// Or just format a message
const message = formatBountyNotification(15);
console.log(message); // "🎯 Bounty Alert: 15 New Opportunities were Found"
```

## Testing

```bash
npm test
```

## Notification Format

The notification system automatically handles proper grammar:

- Single opportunity: "🎯 Bounty Alert: 1 New Opportunity was Found"
- Multiple opportunities: "🎯 Bounty Alert: 15 New Opportunities were Found"

## Error Handling

The system includes comprehensive error handling for:
- Invalid input types
- Negative numbers
- Null/undefined values
- Service failures

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

[MIT](https://choosealicense.com/licenses/mit/)
