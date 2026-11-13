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

  test('should send alert for 3 opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Fix', reward: 100 },
      { id: 2, title: 'Feature Request', reward: 200 },
      { id: 3, title: 'Security Issue', reward: 500 }
    ];

    const result = await sendBountyAlert(3, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(result.notification.count).toBe(3);
    expect(result.notification.opportunities).toHaveLength(3);
    expect(consoleLogSpy).toHaveBeenCalledWith(
      '[BountyScout] 🎯 Bounty Alert: 3 New Opportunities found'
    );
  });

  test('should send alert for 1 opportunity', async () => {
    const opportunities = [{ id: 1, title: 'Bug Fix', reward: 100 }];

    const result = await sendBountyAlert(1, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    expect(result.notification.count).toBe(1);
  });

  test('should handle 0 opportunities', async () => {
    const result = await sendBountyAlert(0, []);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: No new opportunities found');
    expect(result.notification.count).toBe(0);
  });

  test('should handle empty opportunities array', async () => {
    const result = await sendBountyAlert(5, []);

    expect(result.success).toBe(true);
    expect(result.notification.opportunities).toHaveLength(0);
  });

  test('should handle invalid count', async () => {
    const result = await sendBountyAlert(-1, []);

    expect(result.success).toBe(false);
    expect(result.error).toBe('Invalid opportunity count');
    expect(consoleErrorSpy).toHaveBeenCalled();
  });

  test('should handle non-array opportunities', async () => {
    const result = await sendBountyAlert(3, 'not an array');

    expect(result.success).toBe(false);
    expect(result.error).toBe('Opportunities must be an array');
  });

  test('should include timestamp in notification', async () => {
    const result = await sendBountyAlert(1, [{ id: 1 }]);

    expect(result.success).toBe(true);
    expect(result.notification.timestamp).toBeDefined();
    expect(new Date(result.notification.timestamp).toString()).not.toBe('Invalid Date');
  });

  test('should slice opportunities to match count', async () => {
    const opportunities = [
      { id: 1 },
      { id: 2 },
      { id: 3 },
      { id: 4 },
      { id: 5 }
    ];

    const result = await sendBountyAlert(3, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.opportunities).toHaveLength(3);
    expect(result.notification.opportunities[0].id).toBe(1);
    expect(result.notification.opportunities[2].id).toBe(3);
  });
});
