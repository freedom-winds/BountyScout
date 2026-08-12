const { sendBountyAlert } = require('../src/services/notificationService');

describe('sendBountyAlert', () => {
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

  test('should send alert for 13 opportunities', async () => {
    const opportunities = Array(13).fill({ title: 'Test Bounty', reward: 1000 });
    const result = await sendBountyAlert(13, opportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
    expect(result.count).toBe(13);
    expect(result.opportunities).toHaveLength(13);
    expect(consoleLogSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 13 New Opportunities found');
  });

  test('should send alert for single opportunity', async () => {
    const opportunities = [{ title: 'Test Bounty', reward: 1000 }];
    const result = await sendBountyAlert(1, opportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    expect(result.count).toBe(1);
    expect(result.opportunities).toHaveLength(1);
  });

  test('should handle zero opportunities gracefully', async () => {
    const result = await sendBountyAlert(0, []);
    
    expect(result).toBeUndefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('No new opportunities to notify about');
  });

  test('should handle null count gracefully', async () => {
    const result = await sendBountyAlert(null, []);
    
    expect(result).toBeUndefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('No new opportunities to notify about');
  });

  test('should handle empty opportunities array', async () => {
    const result = await sendBountyAlert(5, []);
    
    expect(result.title).toBe('🎯 Bounty Alert: 5 New Opportunities found');
    expect(result.opportunities).toHaveLength(0);
  });

  test('should handle errors gracefully', async () => {
    await expect(sendBountyAlert(-1, [])).rejects.toThrow();
    expect(consoleErrorSpy).toHaveBeenCalled();
  });
});
