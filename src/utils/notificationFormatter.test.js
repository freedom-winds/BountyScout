const { formatOpportunityMessage } = require('./notificationFormatter');

describe('formatOpportunityMessage', () => {
  test('should return singular form for 1 opportunity', () => {
    expect(formatOpportunityMessage(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should return plural form for multiple opportunities', () => {
    expect(formatOpportunityMessage(12)).toBe('🎯 Bounty Alert: 12 New Opportunities found');
    expect(formatOpportunityMessage(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatOpportunityMessage(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle zero opportunities', () => {
    expect(formatOpportunityMessage(0)).toBe('No new opportunities found');
  });
});
