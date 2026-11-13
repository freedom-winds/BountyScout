const { formatBountyAlertTitle } = require('./notificationFormatter');

describe('formatBountyAlertTitle', () => {
  test('should format singular opportunity correctly', () => {
    expect(formatBountyAlertTitle(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format plural opportunities correctly', () => {
    expect(formatBountyAlertTitle(15)).toBe('🎯 Bounty Alert: 15 New Opportunities found');
    expect(formatBountyAlertTitle(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatBountyAlertTitle(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatBountyAlertTitle(0)).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatBountyAlertTitle('15')).toThrow('Count must be a valid non-negative number');
    expect(() => formatBountyAlertTitle(null)).toThrow('Count must be a valid non-negative number');
    expect(() => formatBountyAlertTitle(undefined)).toThrow('Count must be a valid non-negative number');
    expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a valid non-negative number');
    expect(() => formatBountyAlertTitle(NaN)).toThrow('Count must be a valid non-negative number');
  });
});
