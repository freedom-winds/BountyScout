## Description

Fixes the grammar issue in bounty notifications where "Opportunityies" was displayed instead of the correct singular/plural forms.

## Changes

- ✅ Added `notificationFormatter.js` utility to handle proper singular/plural formatting
- ✅ Implemented `formatOpportunityMessage()` function with grammar rules
- ✅ Added comprehensive unit tests
- ✅ Updated notification system to use the new formatter
- ✅ Handles edge cases (0, 1, and multiple opportunities)

## Testing

- [x] Unit tests pass
- [x] Manual testing completed
- [x] Edge cases covered (0, 1, 2, 12, 100 opportunities)

## Examples

**Before:**
```
🎯 Bounty Alert: 12 New Opportunityies found
```

**After:**
```
🎯 Bounty Alert: 12 New Opportunities found
🎯 Bounty Alert: 1 New Opportunity found
```

## Checklist

- [x] Code follows project conventions
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes
