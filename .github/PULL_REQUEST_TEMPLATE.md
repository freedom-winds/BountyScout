## Description

Fixes the typo in bounty notification messages where "Opportunityies" was misspelled.

## Changes Made

- ✅ Created `notificationFormatter.js` utility to handle proper grammar for opportunity notifications
- ✅ Implemented singular/plural handling ("Opportunity" vs "Opportunities")
- ✅ Added proper verb conjugation ("was" vs "were")
- ✅ Created `notificationService.js` for sending notifications
- ✅ Added comprehensive unit tests for both modules
- ✅ Added error handling for edge cases
- ✅ Updated documentation

## Testing

- [x] All tests pass
- [x] Added unit tests for notification formatting
- [x] Added unit tests for notification service
- [x] Tested edge cases (0, 1, multiple opportunities)
- [x] Tested error handling

## Examples

```javascript
formatOpportunityNotification(1)   // "🎯 Bounty Alert: 1 New Opportunity was found"
formatOpportunityNotification(15)  // "🎯 Bounty Alert: 15 New Opportunities were found"
formatOpportunityNotification(0)   // "🎯 Bounty Alert: 0 New Opportunities were found"
```

## Checklist

- [x] Code follows project conventions
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Error handling implemented
