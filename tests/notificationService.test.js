const { sendBountyAlert } = require('../src/services/notificationService');

describe('sendBountyAlert', () => {
  let consoleLogSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
  });

  test('should send notification for single opportunity', async () => {
    const opportunities = [{ id: 1, title: 'Test Bounty' }];
    const result = await sendBountyAlert(opportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    expect(result.opportunities).toEqual(opportunities);
    expect(result.timestamp).toBeDefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('Sending notification: 🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should send notification for multiple opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bounty 1' },
      { id: 2, title: 'Bounty 2' },
      { id: 3, title: 'Bounty 3' }
    ];
    const result = await sendBountyAlert(opportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(result.opportunities).toEqual(opportunities);
    expect(result.timestamp).toBeDefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('Sending notification: 🎯 Bounty Alert: 3 New Opportunities found');
  });

  test('should handle empty opportunities array', async () => {
    const opportunities = [];
    const result = await sendBountyAlert(opportunities);
    
    expect(result).toBeUndefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('No new opportunities to notify about');
  });

  test('should include custom notification config', async () => {
    const opportunities = [{ id: 1, title: 'Test Bounty' }];
    const config = { channel: 'slack', priority: 'high' };
    const result = await sendBountyAlert(opportunities, config);
    
    expect(result.channel).toBe('slack');
    expect(result.priority).toBe('high');
  });

  test('should throw error for non-array input', async () => {
    await expect(sendBountyAlert('not an array')).rejects.toThrow('Opportunities must be an array');
  });

  test('should throw error for null input', async () => {
    await expect(sendBountyAlert(null)).rejects.toThrow('Opportunities must be an array');
  });

  test('should include valid ISO timestamp', async () => {
    const opportunities = [{ id: 1, title: 'Test Bounty' }];
    const result = await sendBountyAlert(opportunities);
    
    const timestamp = new Date(result.timestamp);
    expect(timestamp.toISOString()).toBe(result.timestamp);
    expect(timestamp.getTime()).toBeLessThanOrEqual(Date.now());
  });
});
