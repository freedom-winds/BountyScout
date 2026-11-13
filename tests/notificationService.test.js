const { sendBountyAlert, formatNotificationMessage } = require('../src/services/notificationService');

describe('formatNotificationMessage', () => {
  test('formats opportunities correctly', () => {
    const opportunities = [
      { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' },
      { title: 'Bug Bounty 2', reward: '$1000', platform: 'Bugcrowd' }
    ];
    
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('Bug Bounty 1');
    expect(result).toContain('$500');
    expect(result).toContain('HackerOne');
  });
  
  test('handles missing fields gracefully', () => {
    const opportunities = [
      { title: 'Bug Bounty 1' },
      { reward: '$500' }
    ];
    
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('Bug Bounty 1');
    expect(result).toContain('N/A');
    expect(result).toContain('Untitled');
  });
  
  test('truncates long lists', () => {
    const opportunities = Array(15).fill({ title: 'Test', reward: '$100', platform: 'Test' });
    
    const result = formatNotificationMessage(opportunities);
    expect(result).toContain('... and 5 more');
  });
});

describe('sendBountyAlert', () => {
  test('throws error for non-array input', async () => {
    await expect(sendBountyAlert('not an array')).rejects.toThrow('Opportunities must be an array');
  });
  
  test('handles empty array gracefully', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    await sendBountyAlert([]);
    expect(consoleSpy).toHaveBeenCalledWith('No new opportunities to notify about');
    consoleSpy.mockRestore();
  });
});
