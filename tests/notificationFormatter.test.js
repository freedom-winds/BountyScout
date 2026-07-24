const { formatBountyNotification } = require('../src/utils/notificationFormatter');

describe('formatBountyNotification', () => {
  test('formats single opportunity correctly', () => {
    const result = formatBountyNotification(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity was found');
  });

  test('formats multiple opportunities correctly', () => {
    const result = formatBountyNotification(12);
    expect(result).toBe('🎯 Bounty Alert: 12 New Opportunities were found');
  });

  test('formats zero opportunities correctly', () => {
    const result = formatBountyNotification(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities were found');
  });

  test('formats large numbers correctly', () => {
    const result = formatBountyNotification(100);
    expect(result).toBe('🎯 Bounty Alert: 100 New Opportunities were found');
  });

  test('throws error for negative numbers', () => {
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
  });

  test('throws error for non-number input', () => {
    expect(() => formatBountyNotification('12')).toThrow('Count must be a non-negative number');
  });

  test('throws error for null input', () => {
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
  });

  test('throws error for undefined input', () => {
    expect(() => formatBountyNotification(undefined)).toThrow('Count must be a non-negative number');
  });
});
