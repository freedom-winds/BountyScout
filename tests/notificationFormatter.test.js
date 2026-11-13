const { formatBountyNotification } = require('../src/utils/notificationFormatter');

describe('formatBountyNotification', () => {
  test('formats single opportunity correctly', () => {
    const result = formatBountyNotification(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });
  
  test('formats multiple opportunities correctly', () => {
    const result = formatBountyNotification(15);
    expect(result).toBe('🎯 Bounty Alert: 15 New Opportunities found');
  });
  
  test('formats zero opportunities correctly', () => {
    const result = formatBountyNotification(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });
  
  test('formats large numbers correctly', () => {
    const result = formatBountyNotification(100);
    expect(result).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });
  
  test('throws error for invalid input', () => {
    expect(() => formatBountyNotification('invalid')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyNotification(null)).toThrow('Count must be a non-negative number');
  });
});
