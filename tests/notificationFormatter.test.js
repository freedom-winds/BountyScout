const { formatBountyNotification } = require('../src/utils/notificationFormatter');

describe('formatBountyNotification', () => {
  test('formats singular opportunity correctly', () => {
    const result = formatBountyNotification(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity was Found');
  });

  test('formats plural opportunities correctly', () => {
    const result = formatBountyNotification(15);
    expect(result).toBe('🎯 Bounty Alert: 15 New Opportunities were Found');
  });

  test('handles zero opportunities', () => {
    const result = formatBountyNotification(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities were Found');
  });

  test('handles large numbers', () => {
    const result = formatBountyNotification(1000);
    expect(result).toBe('🎯 Bounty Alert: 1000 New Opportunities were Found');
  });

  test('throws error for negative numbers', () => {
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
  });

  test('throws error for non-numeric input', () => {
    expect(() => formatBountyNotification('15')).toThrow('Count must be a non-negative number');
  });

  test('throws error for null input', () => {
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
  });

  test('throws error for undefined input', () => {
    expect(() => formatBountyNotification(undefined)).toThrow('Count must be a non-negative number');
  });
});
