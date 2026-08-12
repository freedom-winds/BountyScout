const { formatBountyAlertTitle } = require('../src/utils/notificationFormatter');

describe('formatBountyAlertTitle', () => {
  test('should format singular opportunity correctly', () => {
    const result = formatBountyAlertTitle(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format plural opportunities correctly', () => {
    const result = formatBountyAlertTitle(13);
    expect(result).toBe('🎯 Bounty Alert: 13 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    const result = formatBountyAlertTitle(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('should handle large numbers', () => {
    const result = formatBountyAlertTitle(1000);
    expect(result).toBe('🎯 Bounty Alert: 1000 New Opportunities found');
  });

  test('should throw error for negative numbers', () => {
    expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
  });

  test('should throw error for non-number input', () => {
    expect(() => formatBountyAlertTitle('13')).toThrow('Count must be a non-negative number');
  });

  test('should throw error for null input', () => {
    expect(() => formatBountyAlertTitle(null)).toThrow('Count must be a non-negative number');
  });
});
