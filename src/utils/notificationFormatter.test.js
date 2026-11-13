const { formatBountyAlertTitle } = require('./notificationFormatter');

describe('formatBountyAlertTitle', () => {
  test('should format single opportunity correctly', () => {
    expect(formatBountyAlertTitle(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format multiple opportunities correctly', () => {
    expect(formatBountyAlertTitle(3)).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(formatBountyAlertTitle(10)).toBe('🎯 Bounty Alert: 10 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatBountyAlertTitle(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle('3')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(null)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(undefined)).toThrow('Count must be a non-negative number');
  });
});
