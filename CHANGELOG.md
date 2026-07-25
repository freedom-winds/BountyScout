# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2024-01-XX

### Fixed
- Fixed typo in notification messages: "Opportunityies" → "Opportunities"
- Added proper singular/plural handling for opportunity count
- Improved input validation with error handling
- Added comprehensive test coverage for notification formatting

### Added
- `formatBountyNotification` utility function with proper grammar handling
- `sendBountyNotification` service for multi-channel notifications
- Unit tests for notification formatter and service
- Error handling for edge cases (negative numbers, invalid inputs)
- Support for multiple notification channels

### Changed
- Refactored notification system for better maintainability
- Updated documentation with usage examples

## [1.0.0] - 2024-01-XX

### Added
- Initial release of BountyScout
- Basic bounty opportunity detection
- Notification system
