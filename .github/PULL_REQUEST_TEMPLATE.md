## Description

Fixes the typo in bounty notification messages:
- Changed "Opportunityies" to "Opportunities"
- Added proper singular/plural handling
- Added proper verb conjugation (was/were)

## Changes Made

- ✅ Created `notificationFormatter.js` utility for proper message formatting
- ✅ Added comprehensive unit tests
- ✅ Created `notificationService.js` for sending notifications
- ✅ Added error handling for edge cases
- ✅ Updated documentation

## Testing

- [x] All tests pass
- [x] Handles singular case (1 Opportunity)
- [x] Handles plural case (2+ Opportunities)
- [x] Handles edge cases (0, negative, invalid input)
- [x] Proper grammar and spelling

## Examples

```javascript
formatBountyNotification(1)   // "🎯 Bounty Alert: 1 New Opportunity was found"
formatBountyNotification(15)  // "🎯 Bounty Alert: 15 New Opportunities were found"
```

## Checklist

- [x] Code follows project conventions
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Ready for production
