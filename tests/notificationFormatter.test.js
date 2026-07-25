const { formatBountyAlertTitle, validateCount } = require('../src/utils/notificationFormatter');

describe('notificationFormatter', () => {
  describe('formatBountyAlertTitle', () => {
    test('should format title with singular "Opportunity" for count 1', () => {
      const result = formatBountyAlertTitle(1);
      expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should format title with plural "Opportunities" for count > 1', () => {
      const result = formatBountyAlertTitle(3);
      expect(result).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    });

    test('should format title with plural "Opportunities" for count 0', () => {
      const result = formatBountyAlertTitle(0);
      expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
    });

    test('should handle large numbers correctly', () => {
      const result = formatBountyAlertTitle(100);
      expect(result).toBe('🎯 Bounty Alert: 100 New Opportunities found');
    });

    test('should throw error for negative numbers', () => {
      expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
    });

    test('should throw error for non-number input', () => {
      expect(() => formatBountyAlertTitle('invalid')).toThrow('Count must be a non-negative number');
    });
  });

  describe('validateCount', () => {
    test('should return valid number as-is', () => {
      expect(validateCount(5)).toBe(5);
    });

    test('should parse string numbers', () => {
      expect(validateCount('10')).toBe(10);
    });

    test('should return 0 for invalid input', () => {
      expect(validateCount('invalid')).toBe(0);
      expect(validateCount(null)).toBe(0);
      expect(validateCount(undefined)).toBe(0);
    });

    test('should return 0 for negative numbers', () => {
      expect(validateCount(-5)).toBe(0);
    });
  });
});
