## Description

Fixes #[issue number]

This PR fixes the typo in bounty notification messages:
- Changed "Opportunityies" to "Opportunities"
- Added proper singular/plural handling
- Implemented grammar-aware verb conjugation (was/were)
- Added comprehensive error handling
- Included unit tests for all scenarios

## Changes Made

- ✅ Created `notificationFormatter.js` utility for proper message formatting
- ✅ Created `notificationService.js` for sending notifications
- ✅ Added comprehensive unit tests
- ✅ Added error handling for edge cases
- ✅ Updated documentation

## Testing

- [x] All tests pass
- [x] Added tests for singular/plural cases
- [x] Added tests for error handling
- [x] Verified grammar correctness

## Examples

```javascript
formatBountyNotification(1)   // "🎯 Bounty Alert: 1 New Opportunity was Found"
formatBountyNotification(15)  // "🎯 Bounty Alert: 15 New Opportunities were Found"
```
