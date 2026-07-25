## Description

Fixes typo in bounty alert notification message.

## Changes

- Fixed spelling: "Opportunityies" → "Opportunities"
- Added proper singular/plural handling for opportunity count
- Implemented `formatBountyNotification` utility function
- Added comprehensive error handling
- Created unit tests for notification formatting
- Updated notification service to use the formatter

## Testing

- [x] Unit tests added and passing
- [x] Manual testing completed
- [x] Edge cases covered (0, 1, multiple opportunities)
- [x] Error handling tested

## Screenshots

Before: `🎯 Bounty Alert: 15 New Opportunityies found`
After: `🎯 Bounty Alert: 15 New Opportunities found`

## Checklist

- [x] Code follows project style guidelines
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes
- [x] Ready for review
