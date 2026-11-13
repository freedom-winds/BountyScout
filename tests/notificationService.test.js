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

  test('should send alert for 12 opportunities', async () => {
    const opportunities = Array(12).fill({ title: 'Test Bounty' });
    const result = await sendBountyAlert(12, opportunities);
    
    expect(result.success).toBe(true);
    expect(result.count).toBe(12);
    expect(result.title).toBe('🎯 Bounty Alert: 12 New Opportunities found');
    expect(consoleLogSpy).toHaveBeenCalledWith('🎯 Bounty Alert: 12 New Opportunities found');
  });

  test('should send alert for 1 opportunity', async () => {
    const opportunities = [{ title: 'Single Bounty' }];
    const result = await sendBountyAlert(1, opportunities);
    
    expect(result.success).toBe(true);
    expect(result.count).toBe(1);
    expect(result.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should handle zero opportunities gracefully', async () => {
    const result = await sendBountyAlert(0, []);
    
    expect(result).toBeUndefined();
    expect(consoleLogSpy).toHaveBeenCalledWith('No new opportunities to notify about');
  });

  test('should handle missing opportunities array', async () => {
    const result = await sendBountyAlert(5);
    
    expect(result.success).toBe(true);
    expect(result.count).toBe(5);
  });

  test('should log opportunity titles when provided', async () => {
    const opportunities = [
      { title: 'Bounty 1' },
      { title: 'Bounty 2' },
      { title: 'Bounty 3' }
    ];
    
    await sendBountyAlert(3, opportunities);
    
    expect(consoleLogSpy).toHaveBeenCalledWith(
      'Opportunities:',
      'Bounty 1, Bounty 2, Bounty 3'
    );
  });
});
