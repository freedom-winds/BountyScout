const { formatBountyAlertTitle } = require('../src/utils/notificationFormatter');

describe('formatBountyAlertTitle', () => {
  test('formats title correctly for single opportunity', () => {
    const result = formatBountyAlertTitle(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('formats title correctly for multiple opportunities', () => {
    const result = formatBountyAlertTitle(3);
    expect(result).toBe('🎯 Bounty Alert: 3 New Opportunities found');
  });

  test('formats title correctly for zero opportunities', () => {
    const result = formatBountyAlertTitle(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('formats title correctly for large numbers', () => {
    const result = formatBountyAlertTitle(100);
    expect(result).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('throws error for invalid input', () => {
    expect(() => formatBountyAlertTitle('invalid')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(null)).toThrow('Count must be a non-negative number');
  });
});
