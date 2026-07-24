const { formatBountyNotification } = require('../src/utils/notificationFormatter');

describe('formatBountyNotification', () => {
  test('should format singular opportunity correctly', () => {
    const result = formatBountyNotification(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity was found');
  });

  test('should format plural opportunities correctly', () => {
    const result = formatBountyNotification(12);
    expect(result).toBe('🎯 Bounty Alert: 12 New Opportunities were found');
  });

  test('should handle zero opportunities', () => {
    const result = formatBountyNotification(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities were found');
  });

  test('should handle large numbers', () => {
    const result = formatBountyNotification(1000);
    expect(result).toBe('🎯 Bounty Alert: 1000 New Opportunities were found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatBountyNotification('invalid')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
  });
});
