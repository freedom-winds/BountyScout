const { formatOpportunityMessage } = require('./notificationFormatter');

describe('formatOpportunityMessage', () => {
  test('should return correct message for 0 opportunities', () => {
    expect(formatOpportunityMessage(0)).toBe('🎯 Bounty Alert: No new opportunities found');
  });

  test('should return correct message for 1 opportunity (singular)', () => {
    expect(formatOpportunityMessage(1)).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should return correct message for 2 opportunities (plural)', () => {
    expect(formatOpportunityMessage(2)).toBe('🎯 Bounty Alert: 2 New Opportunities found');
  });

  test('should return correct message for 12 opportunities (plural)', () => {
    expect(formatOpportunityMessage(12)).toBe('🎯 Bounty Alert: 12 New Opportunities found');
  });

  test('should return correct message for large numbers', () => {
    expect(formatOpportunityMessage(100)).toBe('🎯 Bounty Alert: 100 New Opportunities found');
  });
});
