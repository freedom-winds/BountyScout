const { sendBountyNotification } = require('./notificationService');
const { formatOpportunityNotification } = require('../utils/notificationFormatter');

jest.mock('../utils/notificationFormatter');

describe('sendBountyNotification', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    jest.clearAllMocks();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  test('sends notification for multiple opportunities', async () => {
    formatOpportunityNotification.mockReturnValue(
      '🎯 Bounty Alert: 12 New Opportunities were found'
    );

    const opportunities = [
      { title: 'Bug Fix', reward: '$500' },
      { title: 'Feature Request', reward: '$1000' }
    ];

    await sendBountyNotification(12, opportunities);

    expect(formatOpportunityNotification).toHaveBeenCalledWith(12);
    expect(consoleLogSpy).toHaveBeenCalledWith(
      '🎯 Bounty Alert: 12 New Opportunities were found'
    );
  });

  test('handles zero opportunities gracefully', async () => {
    await sendBountyNotification(0, []);

    expect(consoleLogSpy).toHaveBeenCalledWith(
      'No new opportunities to notify about'
    );
    expect(formatOpportunityNotification).not.toHaveBeenCalled();
  });

  test('handles errors gracefully', async () => {
    formatOpportunityNotification.mockImplementation(() => {
      throw new Error('Formatting error');
    });

    await expect(sendBountyNotification(5, [])).rejects.toThrow(
      'Formatting error'
    );
    expect(consoleErrorSpy).toHaveBeenCalled();
  });

  test('works without opportunity details', async () => {
    formatOpportunityNotification.mockReturnValue(
      '🎯 Bounty Alert: 3 New Opportunities were found'
    );

    await sendBountyNotification(3);

    expect(formatOpportunityNotification).toHaveBeenCalledWith(3);
    expect(consoleLogSpy).toHaveBeenCalledWith(
      '🎯 Bounty Alert: 3 New Opportunities were found'
    );
  });
});
