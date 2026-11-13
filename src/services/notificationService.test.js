const { sendBountyNotification } = require('./notificationService');
const { formatOpportunityNotification } = require('../utils/notificationFormatter');

jest.mock('../utils/notificationFormatter');

describe('sendBountyNotification', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  test('sends notification for multiple opportunities', async () => {
    formatOpportunityNotification.mockReturnValue(
      '🎯 Bounty Alert: 15 New Opportunities were found'
    );

    const opportunities = Array(15).fill({ title: 'Test Bounty' });
    const result = await sendBountyNotification(15, opportunities);

    expect(formatOpportunityNotification).toHaveBeenCalledWith(15);
    expect(console.log).toHaveBeenCalledWith(
      '🎯 Bounty Alert: 15 New Opportunities were found'
    );
    expect(result).toEqual({
      success: true,
      message: '🎯 Bounty Alert: 15 New Opportunities were found',
      count: 15,
      opportunities
    });
  });

  test('sends notification for single opportunity', async () => {
    formatOpportunityNotification.mockReturnValue(
      '🎯 Bounty Alert: 1 New Opportunity was found'
    );

    const opportunities = [{ title: 'Test Bounty' }];
    const result = await sendBountyNotification(1, opportunities);

    expect(formatOpportunityNotification).toHaveBeenCalledWith(1);
    expect(result.success).toBe(true);
    expect(result.count).toBe(1);
  });

  test('handles zero opportunities gracefully', async () => {
    await sendBountyNotification(0, []);

    expect(console.log).toHaveBeenCalledWith(
      'No new opportunities to notify about'
    );
    expect(formatOpportunityNotification).not.toHaveBeenCalled();
  });

  test('handles errors properly', async () => {
    formatOpportunityNotification.mockImplementation(() => {
      throw new Error('Formatting error');
    });

    await expect(sendBountyNotification(15, [])).rejects.toThrow(
      'Formatting error'
    );
    expect(console.error).toHaveBeenCalled();
  });

  test('works without opportunities array', async () => {
    formatOpportunityNotification.mockReturnValue(
      '🎯 Bounty Alert: 5 New Opportunities were found'
    );

    const result = await sendBountyNotification(5);

    expect(result.success).toBe(true);
    expect(result.opportunities).toEqual([]);
  });
});
