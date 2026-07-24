const { formatOpportunityMessage } = require('./notificationFormatter');

describe('formatOpportunityMessage', () => {
  test('should format singular opportunity correctly', () => {
    expect(formatOpportunityMessage(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format plural opportunities correctly', () => {
    expect(formatOpportunityMessage(12)).toBe('🎯 Bounty Alert: 12 New Opportunities found');
    expect(formatOpportunityMessage(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatOpportunityMessage(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatOpportunityMessage(0)).toBe('🎯 Bounty Alert: 0 New Opportunities found');
  });

  test('should throw error for invalid input', () => {
    expect(() => formatOpportunityMessage(-1)).toThrow('Count must be a non-negative number');
    expect(() => formatOpportunityMessage('12')).toThrow('Count must be a non-negative number');
    expect(() => formatOpportunityMessage(null)).toThrow('Count must be a non-negative number');
    expect(() => formatOpportunityMessage(undefined)).toThrow('Count must be a non-negative number');
  });
});
