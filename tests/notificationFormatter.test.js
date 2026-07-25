const { formatBountyAlertTitle } = require('../src/utils/notificationFormatter');

describe('formatBountyAlertTitle', () => {
  test('formats single opportunity correctly', () => {
    const result = formatBountyAlertTitle(1);
    expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('formats multiple opportunities correctly', () => {
    const result = formatBountyAlertTitle(3);
    expect(result).toBe('🎯 Bounty Alert: 3 New Opportunities found');
  });

  test('formats zero opportunities correctly', () => {
    const result = formatBountyAlertTitle(0);
    expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('formats large numbers correctly', () => {
    const result = formatBountyAlertTitle(100);
    expect(result).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('throws error for negative numbers', () => {
    expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
  });

  test('throws error for non-number input', () => {
    expect(() => formatBountyAlertTitle('3')).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(null)).toThrow('Count must be a non-negative number');
    expect(() => formatBountyAlertTitle(undefined)).toThrow('Count must be a non-negative number');
  });
});
