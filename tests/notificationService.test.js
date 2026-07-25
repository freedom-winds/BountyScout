const { sendBountyAlert, formatNotificationMessage } = require('../src/services/notificationService');

describe('formatNotificationMessage', () => {
  test('formats single opportunity', () => {
    const opportunities = [
      { title: 'Bug Bounty', reward: '$500', platform: 'HackerOne' }
    ];
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('1. Bug Bounty - $500 (HackerOne)');
  });

  test('formats multiple opportunities', () => {
    const opportunities = [
      { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' },
      { title: 'Bug Bounty 2', reward: '$1000', platform: 'Bugcrowd' },
      { title: 'Bug Bounty 3', reward: '$750', platform: 'Intigriti' }
    ];
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('1. Bug Bounty 1');
    expect(result).toContain('2. Bug Bounty 2');
    expect(result).toContain('3. Bug Bounty 3');
  });

  test('handles opportunities without reward', () => {
    const opportunities = [
      { title: 'Bug Bounty', platform: 'HackerOne' }
    ];
    const result = formatNotificationMessage(opportunities);
    expect(result).toBe('1. Bug Bounty (HackerOne)');
  });

  test('handles opportunities without platform', () => {
    const opportunities = [
      { title: 'Bug Bounty', reward: '$500' }
    ];
    const result = formatNotificationMessage(opportunities);
    expect(result).toBe('1. Bug Bounty - $500');
  });

  test('limits display to 5 opportunities', () => {
    const opportunities = Array.from({ length: 10 }, (_, i) => ({
      title: `Bug Bounty ${i + 1}`,
      reward: '$500',
      platform: 'HackerOne'
    }));
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('...and 5 more');
    expect(result).toContain('1. Bug Bounty 1');
    expect(result).toContain('5. Bug Bounty 5');
    expect(result).not.toContain('6. Bug Bounty 6');
  });

  test('handles empty array', () => {
    const result = formatNotificationMessage([]);
    expect(result).toBe('No opportunities available');
  });

  test('handles untitled opportunities', () => {
    const opportunities = [
      { reward: '$500', platform: 'HackerOne' }
    ];
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('1. Untitled - $500 (HackerOne)');
  });
});

describe('sendBountyAlert', () => {
  test('throws error for non-array input', async () => {
    await expect(sendBountyAlert('not an array')).rejects.toThrow('Opportunities must be an array');
  });

  test('handles empty opportunities array', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    await sendBountyAlert([]);
    expect(consoleSpy).toHaveBeenCalledWith('No new opportunities to notify about');
    consoleSpy.mockRestore();
  });

  test('sends notification for valid opportunities', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    const opportunities = [
      { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' },
      { title: 'Bug Bounty 2', reward: '$1000', platform: 'Bugcrowd' },
      { title: 'Bug Bounty 3', reward: '$750', platform: 'Intigriti' }
    ];
    
    await sendBountyAlert(opportunities);
    
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining('Notification sent: 🎯 Bounty Alert: 3 New Opportunities found')
    );
    consoleSpy.mockRestore();
  });
});
