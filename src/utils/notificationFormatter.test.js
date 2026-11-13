const { formatOpportunityNotification } = require('./notificationFormatter');

describe('formatOpportunityNotification', () => {
  test('formats single opportunity correctly', () => {
    expect(formatOpportunityNotification(1)).toBe(
      '🎯 Bounty Alert: 1 New Opportunity was found'
    );
  });

  test('formats multiple opportunities correctly', () => {
    expect(formatOpportunityNotification(12)).toBe(
      '🎯 Bounty Alert: 12 New Opportunities were found'
    );
  });

  test('formats zero opportunities correctly', () => {
    expect(formatOpportunityNotification(0)).toBe(
      '🎯 Bounty Alert: 0 New Opportunities were found'
    );
  });

  test('formats large numbers correctly', () => {
    expect(formatOpportunityNotification(100)).toBe(
      '🎯 Bounty Alert: 100 New Opportunities were found'
    );
  });

  test('throws error for negative numbers', () => {
    expect(() => formatOpportunityNotification(-1)).toThrow(
      'Count must be a non-negative number'
    );
  });

  test('throws error for non-number input', () => {
    expect(() => formatOpportunityNotification('12')).toThrow(
      'Count must be a non-negative number'
    );
  });

  test('throws error for null input', () => {
    expect(() => formatOpportunityNotification(null)).toThrow(
      'Count must be a non-negative number'
    );
  });
});
