const NotificationService = require('../src/services/notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    jest.spyOn(console, 'log').mockImplementation();
    jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should send bounty alert with correct title for multiple opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix' },
      { id: 2, title: 'Feature Request' }
    ];

    const result = await service.sendBountyAlert(2, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
    expect(result.notification.count).toBe(2);
    expect(result.notification.opportunities).toHaveLength(2);
  });

  test('should send bounty alert with correct title for single opportunity', async () => {
    const opportunities = [{ id: 1, title: 'Bug Fix' }];

    const result = await service.sendBountyAlert(1, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
  });

  test('should handle zero opportunities gracefully', async () => {
    const result = await service.sendBountyAlert(0, []);

    expect(result.success).toBe(true);
    expect(result.message).toBe('No new opportunities to notify');
  });

  test('should include timestamp in notification', async () => {
    const result = await service.sendBountyAlert(5, []);

    expect(result.notification.timestamp).toBeDefined();
    expect(new Date(result.notification.timestamp)).toBeInstanceOf(Date);
  });

  test('should handle errors gracefully', async () => {
    const result = await service.sendBountyAlert(-1, []);

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });

  test('should limit opportunities to count specified', async () => {
    const opportunities = [
      { id: 1, title: 'Bug 1' },
      { id: 2, title: 'Bug 2' },
      { id: 3, title: 'Bug 3' }
    ];

    const result = await service.sendBountyAlert(2, opportunities);

    expect(result.notification.opportunities).toHaveLength(2);
  });
});
