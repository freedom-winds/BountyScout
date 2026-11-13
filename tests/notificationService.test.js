const { sendBountyNotification } = require('../src/services/notificationService');

describe('sendBountyNotification', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  test('sends notification for single opportunity', async () => {
    const message = await sendBountyNotification(1, [{ id: 1 }]);
    expect(message).toBe('🎯 Bounty Alert: 1 New Opportunity was Found');
    expect(consoleLogSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 1 New Opportunity was Found');
  });

  test('sends notification for multiple opportunities', async () => {
    const opportunities = Array(15).fill({ id: 1 });
    const message = await sendBountyNotification(15, opportunities);
    expect(message).toBe('🎯 Bounty Alert: 15 New Opportunities were Found');
    expect(consoleLogSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 15 New Opportunities were Found');
  });

  test('handles zero opportunities gracefully', async () => {
    await sendBountyNotification(0, []);
    expect(consoleLogSpy).toHaveBeenCalledWith('No new opportunities to notify about');
  });

  test('handles errors gracefully', async () => {
    await expect(sendBountyNotification(-1)).rejects.toThrow();
    expect(consoleErrorSpy).toHaveBeenCalled();
  });
});
