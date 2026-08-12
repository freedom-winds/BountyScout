# BountyScout

Automated bounty hunting opportunity scout.

## Features

- 🎯 Real-time bounty opportunity detection
- 📢 Smart notification system with proper pluralization
- 🔍 Automated scanning and filtering
- 📊 Opportunity tracking and reporting

## Installation

```bash
npm install
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');
const { formatBountyAlertTitle } = require('./src/utils/notificationFormatter');

// Send a bounty alert
await sendBountyAlert(13, opportunities);

// Format a notification title
const title = formatBountyAlertTitle(13);
// Output: "🎯 Bounty Alert: 13 New Opportunities found"
```

## Testing

```bash
npm test
```

## Notification Format

The notification system automatically handles singular and plural forms:

- 1 opportunity: "🎯 Bounty Alert: 1 New Opportunity found"
- Multiple opportunities: "🎯 Bounty Alert: 13 New Opportunities found"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
