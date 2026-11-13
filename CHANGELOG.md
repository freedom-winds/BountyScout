# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-01-XX

### Fixed
- Fixed typo in notification message: "Opportunityies" → "Opportunities"
- Added proper singular/plural handling for opportunity notifications
- Implemented correct verb conjugation ("was" vs "were") based on count

### Added
- Created `notificationFormatter` utility with proper grammar rules
- Added comprehensive test suite for notification formatting
- Added `notificationService` for handling bounty notifications
- Added error handling for invalid input

### Changed
- Improved notification message formatting
- Enhanced code structure with proper separation of concerns
