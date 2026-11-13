const { sendBountyAlert, formatNotificationMessage } = require('../src/services/notificationService');

describe('notificationService', () => {
  describe('formatNotificationMessage', () => {
    test('formats single opportunity', () => {
      const opportunities = [
        { title: 'Bug Bounty', reward: '$500', platform: 'HackerOne' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Bug Bounty - $500 [HackerOne]');
    });

    test('formats multiple opportunities', () => {
      const opportunities = [
        { title: 'Bug Bounty 1', reward: '$500', platform: 'HackerOne' },
        { title: 'Bug Bounty 2', reward: '$1000', platform: 'Bugcrowd' },
        { title: 'Bug Bounty 3', reward: '$750', platform: 'Synack' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Bug Bounty 1');
      expect(result).toContain('2. Bug Bounty 2');
      expect(result).toContain('3. Bug Bounty 3');
    });

    test('handles opportunities without reward or platform', () => {
      const opportunities = [
        { title: 'Bug Bounty' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toBe('1. Bug Bounty');
    });

    test('truncates long lists and shows count', () => {
      const opportunities = Array.from({ length: 10 }, (_, i) => ({
        title: `Bug Bounty ${i + 1}`,
        reward: '$500'
      }));
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('... and 5 more');
    });

    test('handles empty title', () => {
      const opportunities = [
        { reward: '$500', platform: 'HackerOne' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Untitled - $500 [HackerOne]');
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

    test('processes valid opportunities', async () => {
      const opportunities = [
        { title: 'Bug Bounty', reward: '$500', platform: 'HackerOne' }
      ];
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      await sendBountyAlert(opportunities);
      
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Successfully sent notification for 1 opportunities')
      );
      consoleSpy.mockRestore();
    });
  });
});
