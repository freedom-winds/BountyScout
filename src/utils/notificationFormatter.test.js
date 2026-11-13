const { formatOpportunityNotification } = require('./notificationFormatter');

describe('formatOpportunityNotification', () => {
  test('should format singular opportunity correctly', () => {
    expect(formatOpportunityNotification(1)).toBe(
      '🎯 Bounty Alert: 1 New Opportunity was found'
    );
  });

  test('should format plural opportunities correctly', () => {
    expect(formatOpportunityNotification(12)).toBe(
      '🎯 Bounty Alert: 12 New Opportunities were found'
    );
  });

  test('should handle zero opportunities', () => {
    expect(formatOpportunityNotification(0)).toBe(
      '🎯 Bounty Alert: 0 New Opportunities were found'
    );
  });

  test('should handle large numbers', () => {
    expect(formatOpportunityNotification(100)).toBe(
      '🎯 Bounty Alert: 100 New Opportunities were found'
    );
  });

  test('should throw error for negative numbers', () => {
    expect(() => formatOpportunityNotification(-1)).toThrow(
      'Count must be a non-negative number'
    );
  });

  test('should throw error for non-number input', () => {
    expect(() => formatOpportunityNotification('12')).toThrow(
      'Count must be a non-negative number'
    );
  });
});
