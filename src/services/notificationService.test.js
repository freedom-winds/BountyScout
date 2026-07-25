const { sendBountyAlert } = require('./notificationService');

describe('sendBountyAlert', () => {
  let mockNotificationClient;

  beforeEach(() => {
    mockNotificationClient = {
      send: jest.fn().mockResolvedValue({ id: '123', status: 'sent' })
    };
  });

  test('should send notification with correct title for multiple opportunities', async () => {
    const opportunities = [
      { title: 'Bug Fix', reward: '$500' },
      { title: 'Feature Request', reward: '$1000' },
      { title: 'Security Issue', reward: '$2000' }
    ];

    const result = await sendBountyAlert(3, opportunities, mockNotificationClient);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(mockNotificationClient.send).toHaveBeenCalledWith(
      expect.objectContaining({
        title: '🎯 Bounty Alert: 3 New Opportunities found',
        count: 3
      })
    );
  });

  test('should send notification with correct title for single opportunity', async () => {
    const opportunities = [
      { title: 'Bug Fix', reward: '$500' }
    ];

    const result = await sendBountyAlert(1, opportunities, mockNotificationClient);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should format message with opportunity details', async () => {
    const opportunities = [
      { title: 'Bug Fix', reward: '$500' },
      { title: 'Feature Request', reward: '$1000' }
    ];

    const result = await sendBountyAlert(2, opportunities, mockNotificationClient);

    expect(result.notification.message).toContain('1. Bug Fix - $500');
    expect(result.notification.message).toContain('2. Feature Request - $1000');
  });

  test('should handle empty opportunities array', async () => {
    const result = await sendBountyAlert(0, [], mockNotificationClient);

    expect(result.success).toBe(true);
    expect(result.notification.message).toBe('Check the dashboard for details.');
  });

  test('should handle opportunities without title or reward', async () => {
    const opportunities = [
      { title: 'Bug Fix' },
      { reward: '$1000' },
      {}
    ];

    const result = await sendBountyAlert(3, opportunities, mockNotificationClient);

    expect(result.success).toBe(true);
    expect(result.notification.message).toContain('1. Bug Fix - N/A');
    expect(result.notification.message).toContain('2. Untitled - $1000');
    expect(result.notification.message).toContain('3. Untitled - N/A');
  });

  test('should handle notification client errors', async () => {
    mockNotificationClient.send.mockRejectedValue(new Error('Network error'));

    const result = await sendBountyAlert(3, [], mockNotificationClient);

    expect(result.success).toBe(false);
    expect(result.error).toBe('Network error');
  });

  test('should throw error when notification client is missing', async () => {
    const result = await sendBountyAlert(3, []);

    expect(result.success).toBe(false);
    expect(result.error).toBe('Notification client is required');
  });

  test('should throw error when opportunities is not an array', async () => {
    const result = await sendBountyAlert(3, 'not an array', mockNotificationClient);

    expect(result.success).toBe(false);
    expect(result.error).toBe('Opportunities must be an array');
  });

  test('should include timestamp in notification', async () => {
    const result = await sendBountyAlert(1, [], mockNotificationClient);

    expect(result.success).toBe(true);
    expect(result.notification.timestamp).toBeDefined();
    expect(new Date(result.notification.timestamp).toString()).not.toBe('Invalid Date');
  });
});
