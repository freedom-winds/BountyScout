## Description

Fixes the typo in bounty notification messages where "Opportunityies" was misspelled.

## Changes Made

- Created `notificationFormatter.js` utility to format bounty notifications with proper grammar
- Implemented singular/plural handling for "Opportunity" vs "Opportunities"
- Added comprehensive unit tests for the formatter
- Created `notificationService.js` for sending notifications
- Added error handling for edge cases (negative numbers, invalid types)
- Updated documentation in README.md

## Testing

- ✅ Unit tests for `formatBountyNotification`
- ✅ Unit tests for `sendBountyNotification`
- ✅ Edge case handling (0, 1, multiple opportunities)
- ✅ Error handling for invalid inputs

## Fixes

- Fixes #[issue-number] - Corrects "Opportunityies" typo to "Opportunities"
- Implements proper singular/plural grammar rules

## Checklist

- [x] Code follows project conventions
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Error handling implemented
