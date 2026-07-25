const { sendBountyAlert } = require('./notificationService');

describe('sendBountyAlert', () => {
  beforeEach(() => {
    jest.spyOn(console, 'log').mockImplementation();
    jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should send notification with correct title for multiple opportunities', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Bounty 1', url: 'https://example.com/1', reward: '$500', platform: 'HackerOne' },
      { id: 2, title: 'Bug Bounty 2', url: 'https://example.com/2', reward: '$1000', platform: 'Bugcrowd' },
      { id: 3, title: 'Bug Bounty 3', url: 'https://example.com/3', reward: '$750', platform: 'Intigriti' }
    ];

    const result = await sendBountyAlert(3, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 3 New Opportunities found');
    expect(result.notification.count).toBe(3);
    expect(result.notification.opportunities).toHaveLength(3);
  });

  test('should send notification with correct title for single opportunity', async () => {
    const opportunities = [
      { id: 1, title: 'Bug Bounty 1', url: 'https://example.com/1', reward: '$500', platform: 'HackerOne' }
    ];

    const result = await sendBountyAlert(1, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    expect(result.notification.count).toBe(1);
  });

  test('should handle empty opportunities array', async () => {
    const result = await sendBountyAlert(0, []);

    expect(result.success).toBe(true);
    expect(result.notification.title).toBe('🎯 Bounty Alert: No new opportunities found');
    expect(result.notification.opportunities).toHaveLength(0);
  });

  test('should sanitize opportunity data with missing fields', async () => {
    const opportunities = [
      { title: 'Incomplete Bounty' },
      {}
    ];

    const result = await sendBountyAlert(2, opportunities);

    expect(result.success).toBe(true);
    expect(result.notification.opportunities[0]).toEqual({
      id: null,
      title: 'Incomplete Bounty',
      url: null,
      reward: null,
      platform: 'Unknown'
    });
    expect(result.notification.opportunities[1]).toEqual({
      id: null,
      title: 'Untitled',
      url: null,
      reward: null,
      platform: 'Unknown'
    });
  });

  test('should handle invalid opportunities input', async () => {
    const result = await sendBountyAlert(3, 'not an array');

    expect(result.success).toBe(false);
    expect(result.error).toBe('Opportunities must be an array');
  });

  test('should include timestamp in notification', async () => {
    const result = await sendBountyAlert(1, []);

    expect(result.success).toBe(true);
    expect(result.notification.timestamp).toBeDefined();
    expect(new Date(result.notification.timestamp)).toBeInstanceOf(Date);
  });

  test('should merge additional options', async () => {
    const options = {
      priority: 'high',
      channel: 'slack'
    };

    const result = await sendBountyAlert(2, [], options);

    expect(result.success).toBe(true);
    expect(result.notification.priority).toBe('high');
    expect(result.notification.channel).toBe('slack');
  });
});
