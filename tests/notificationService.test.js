const { sendBountyAlert } = require('../src/services/notificationService');

describe('sendBountyAlert', () => {
  test('sends alert for multiple opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 },
      { id: 2, title: 'Feature Request', reward: 200 },
      { id: 3, title: 'Security Issue', reward: 500 }
    ];

    const result = await sendBountyAlert(opportunities);
    
    expect(result).toBeDefined();
    expect(result.title).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(result.opportunities).toEqual(opportunities);
    expect(result.timestamp).toBeDefined();
  });

  test('sends alert for single opportunity', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 }
    ];

    const result = await sendBountyAlert(opportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('handles empty opportunities array', async () => {
    const opportunities = [];
    const consoleSpy = jest.spyOn(console, 'log');

    const result = await sendBountyAlert(opportunities);
    
    expect(result).toBeUndefined();
    expect(consoleSpy).toHaveBeenCalledWith('No new opportunities to notify about');
    
    consoleSpy.mockRestore();
  });

  test('throws error for invalid input', async () => {
    await expect(sendBountyAlert('invalid')).rejects.toThrow('Opportunities must be an array');
    await expect(sendBountyAlert(null)).rejects.toThrow('Opportunities must be an array');
  });

  test('includes custom options in notification', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 }
    ];
    const options = {
      channel: 'slack',
      priority: 'high'
    };

    const result = await sendBountyAlert(opportunities, options);
    
    expect(result.channel).toBe('slack');
    expect(result.priority).toBe('high');
  });
});
