const { formatOpportunityNotification } = require('./notificationFormatter');

describe('formatOpportunityNotification', () => {
  test('should return correct message for 0 opportunities', () => {
    expect(formatOpportunityNotification(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('should return correct message for 1 opportunity (singular)', () => {
    expect(formatOpportunityNotification(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should return correct message for 2 opportunities (plural)', () => {
    expect(formatOpportunityNotification(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
  });

  test('should return correct message for 3 opportunities (plural)', () => {
    expect(formatOpportunityNotification(3)).toBe('🎯 Bounty Alert: 3 New Opportunities found');
  });

  test('should return correct message for large numbers', () => {
    expect(formatOpportunityNotification(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });
});
