const { sendBountyAlert } = require('../src/services/notificationService');

describe('sendBountyAlert', () => {
  beforeEach(() => {
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should send notification for multiple opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 },
      { id: 2, title: 'Feature Request', reward: 200 }
    ];
    
    const result = await sendBountyAlert(2, opportunities);
    
    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(result.notification.count).toBe(2);
    expect(result.notification.opportunities).toHaveLength(2);
  });

  test('should handle zero opportunities', async () => {
    const result = await sendBountyAlert(0, []);
    
    expect(result.success).toBe(true);
    expect(result.message).toBe('No notifications sent');
  });

  test('should limit opportunities in notification to 10', async () => {
    const opportunities = Array.from({ length: 20 }, (_, i) => ({
      id: i + 1,
      title: `Opportunity ${i + 1}`,
      reward: 100
    }));
    
    const result = await sendBountyAlert(20, opportunities);
    
    expect(result.success).toBe(true);
    expect(result.notification.opportunities).toHaveLength(10);
  });

  test('should handle errors gracefully', async () => {
    // Force an error by passing invalid data that will cause formatBountyAlertTitle to throw
    const result = await sendBountyAlert('invalid');
    
    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });
});
