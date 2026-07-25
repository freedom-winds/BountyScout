const { formatOpportunityMessage } = require('./notificationFormatter');

describe('formatOpportunityMessage', () => {
  test('should return correct message for 0 opportunities', () => {
    expect(formatOpportunityMessage(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('should return singular form for 1 opportunity', () => {
    expect(formatOpportunityMessage(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should return plural form for multiple opportunities', () => {
    expect(formatOpportunityMessage(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(formatOpportunityMessage(15)).toBe('🎯 Bounty Alert: 15 New Opportunities found');
    expect(formatOpportunityMessage(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });

  test('should handle large numbers', () => {
    expect(formatOpportunityMessage(1000)).toBe('🎯 Bounty Alert: 1000 New Opportunities found');
  });
});
