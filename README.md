# BountyScout 🎯

Automated bug bounty opportunity scanner and notification system.

## Features

- 🔍 Scans multiple bug bounty platforms
- 🎯 Real-time notifications for new opportunities
- 📧 Multiple notification channels (Webhook, Email, Slack)
- 🔔 Customizable alert preferences

## Installation

```bash
npm install
```

## Configuration

Create a `config.json` file:

```json
{
  "notifications": {
    "webhook": "https://your-webhook-url.com",
    "slack": {
      "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    },
    "email": {
      "enabled": false
    }
  },
  "platforms": ["HackerOne", "Bugcrowd", "Intigriti"],
  "scanInterval": 3600000
}
```

## Usage

```javascript
const { sendBountyAlert } = require('./src/services/notificationService');

const opportunities = [
  {
    id: '1',
    title: 'XSS Vulnerability',
    reward: '$500',
    url: 'https://example.com/bounty/1',
    platform: 'HackerOne'
  }
];

const config = {
  webhook: 'https://your-webhook-url.com',
  slack: {
    webhookUrl: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
  }
};

await sendBountyAlert(opportunities, config);
```

## Notification Format

Notifications are formatted with proper grammar:
- ✅ "1 New Opportunity found" (singular)
- ✅ "12 New Opportunities found" (plural)
- ❌ "12 New Opportunityies found" (typo fixed)

## Testing

```bash
npm test
```

## API

### `sendBountyAlert(opportunities, config)`

Sends notifications for new bounty opportunities.

**Parameters:**
- `opportunities` (Array): Array of opportunity objects
- `config` (Object): Notification configuration

**Returns:** Promise<Object> - Notification message object

### `formatBountyAlertTitle(count)`

Formats the notification title with correct grammar.

**Parameters:**
- `count` (Number): Number of opportunities

**Returns:** String - Formatted title

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## License

MIT
