const { sendBountyAlert, formatBountyAlertTitle } = require('../src/services/notificationService');
const { formatBountyAlertTitle: formatTitle } = require('../src/utils/notificationFormatter');

describe('sendBountyAlert', () => {
  const mockOpportunities = [
    {
      id: '1',
      title: 'XSS Vulnerability',
      reward: '$500',
      url: 'https://example.com/bounty/1',
      platform: 'HackerOne'
    },
    {
      id: '2',
      title: 'SQL Injection',
      reward: '$1000',
      url: 'https://example.com/bounty/2',
      platform: 'Bugcrowd'
    }
  ];

  test('handles empty opportunities array', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    await sendBountyAlert([]);
    expect(consoleSpy).toHaveBeenCalledWith('No new opportunities to notify about');
    consoleSpy.mockRestore();
  });

  test('throws error for non-array input', async () => {
    await expect(sendBountyAlert('not an array')).rejects.toThrow('Opportunities must be an array');
  });

  test('formats message correctly', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    const result = await sendBountyAlert(mockOpportunities);
    
    expect(result.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(result.count).toBe(2);
    expect(result.opportunities).toHaveLength(2);
    expect(result.timestamp).toBeDefined();
    
    consoleSpy.mockRestore();
  });
});

describe('formatBountyAlertTitle integration', () => {
  test('correctly formats title with typo fix', () => {
    const result = formatTitle(12);
    expect(result).toBe('🎯 Bounty Alert: 12 New Opportunities found');
    expect(result).not.toContain('Opportunityies');
  });
});
