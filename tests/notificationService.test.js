const { sendBountyAlert, formatBountyAlertTitle } = require('../src/services/notificationService');
const { formatBountyAlertTitle: formatter } = require('../src/utils/notificationFormatter');

// Mock node-fetch
jest.mock('node-fetch');
const fetch = require('node-fetch');

describe('notificationService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  describe('sendBountyAlert', () => {
    test('sends notification for multiple opportunities', async () => {
      const opportunities = [
        { title: 'Bug Bounty 1', reward: '$500' },
        { title: 'Bug Bounty 2', reward: '$1000' }
      ];

      const result = await sendBountyAlert(2, opportunities);

      expect(result).toBeDefined();
      expect(result.title).toBe('🎯 Bounty Alert: 2 New Opportunities found');
      expect(result.count).toBe(2);
      expect(console.log).toHaveBeenCalledWith(
        'Sending notification: 🎯 Bounty Alert: 2 New Opportunities found'
      );
    });

    test('handles zero opportunities gracefully', async () => {
      await sendBountyAlert(0, []);

      expect(console.log).toHaveBeenCalledWith('No new opportunities to notify about');
    });

    test('handles missing opportunities array', async () => {
      const result = await sendBountyAlert(5);

      expect(result).toBeDefined();
      expect(result.count).toBe(5);
    });

    test('limits opportunities in notification to 10', async () => {
      const opportunities = Array.from({ length: 20 }, (_, i) => ({
        title: `Bounty ${i + 1}`
      }));

      const result = await sendBountyAlert(20, opportunities);

      expect(result.opportunities).toHaveLength(10);
    });
  });

  describe('Slack notification', () => {
    beforeEach(() => {
      process.env.SLACK_WEBHOOK_URL = 'https://hooks.slack.com/test';
      fetch.mockResolvedValue({ ok: true });
    });

    afterEach(() => {
      delete process.env.SLACK_WEBHOOK_URL;
    });

    test('sends Slack notification when webhook is configured', async () => {
      const opportunities = [{ title: 'Test Bounty' }];

      await sendBountyAlert(1, opportunities);

      expect(fetch).toHaveBeenCalledWith(
        'https://hooks.slack.com/test',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
      );
    });
  });

  describe('Discord notification', () => {
    beforeEach(() => {
      process.env.DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/test';
      fetch.mockResolvedValue({ ok: true });
    });

    afterEach(() => {
      delete process.env.DISCORD_WEBHOOK_URL;
    });

    test('sends Discord notification when webhook is configured', async () => {
      const opportunities = [{ title: 'Test Bounty' }];

      await sendBountyAlert(1, opportunities);

      expect(fetch).toHaveBeenCalledWith(
        'https://discord.com/api/webhooks/test',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
      );
    });
  });
});
