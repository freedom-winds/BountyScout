const { formatBountyAlertTitle, validateOpportunityCount } = require('../src/utils/notificationFormatter');

describe('notificationFormatter', () => {
  describe('formatBountyAlertTitle', () => {
    test('should format title correctly for single opportunity', () => {
      const result = formatBountyAlertTitle(1);
      expect(result).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should format title correctly for multiple opportunities', () => {
      const result = formatBountyAlertTitle(3);
      expect(result).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    });

    test('should format title correctly for zero opportunities', () => {
      const result = formatBountyAlertTitle(0);
      expect(result).toBe('🎯 Bounty Alert: 0 New Opportunities found');
    });

    test('should throw error for negative count', () => {
      expect(() => formatBountyAlertTitle(-1)).toThrow('Count must be a non-negative number');
    });

    test('should throw error for non-number input', () => {
      expect(() => formatBountyAlertTitle('invalid')).toThrow('Count must be a non-negative number');
    });
  });

  describe('validateOpportunityCount', () => {
    test('should return valid number', () => {
      expect(validateOpportunityCount(5)).toBe(5);
    });

    test('should parse string numbers', () => {
      expect(validateOpportunityCount('10')).toBe(10);
    });

    test('should return 0 for invalid input', () => {
      expect(validateOpportunityCount('invalid')).toBe(0);
    });

    test('should return 0 for negative numbers', () => {
      expect(validateOpportunityCount(-5)).toBe(0);
    });

    test('should return 0 for null', () => {
      expect(validateOpportunityCount(null)).toBe(0);
    });

    test('should return 0 for undefined', () => {
      expect(validateOpportunityCount(undefined)).toBe(0);
    });
  });
});
