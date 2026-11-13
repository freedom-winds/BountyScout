const { sendBountyAlert, formatNotificationMessage } = require('../src/services/notificationService');

describe('notificationService', () => {
  describe('formatNotificationMessage', () => {
    test('should format message with opportunities', () => {
      const opportunities = [
        { title: 'Bug Fix', reward: '$500' },
        { title: 'Feature Request', reward: '$1000' },
        { title: 'Security Issue', reward: '$2000' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Bug Fix - $500');
      expect(result).toContain('2. Feature Request - $1000');
      expect(result).toContain('3. Security Issue - $2000');
    });

    test('should handle empty opportunities array', () => {
      const result = formatNotificationMessage([]);
      expect(result).toBe('New bounty opportunities are available!');
    });

    test('should show "and X more" for more than 3 opportunities', () => {
      const opportunities = [
        { title: 'Opp 1' },
        { title: 'Opp 2' },
        { title: 'Opp 3' },
        { title: 'Opp 4' },
        { title: 'Opp 5' }
      ];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('...and 2 more');
    });

    test('should handle opportunities without rewards', () => {
      const opportunities = [{ title: 'Test Opportunity' }];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Test Opportunity');
      expect(result).not.toContain(' - ');
    });

    test('should handle opportunities without titles', () => {
      const opportunities = [{ reward: '$100' }];
      const result = formatNotificationMessage(opportunities);
      expect(result).toContain('1. Untitled - $100');
    });
  });

  describe('sendBountyAlert', () => {
    test('should return success for valid opportunities', async () => {
      const result = await sendBountyAlert(3, [
        { title: 'Test 1' },
        { title: 'Test 2' },
        { title: 'Test 3' }
      ]);
      expect(result.success).toBe(true);
      expect(result.sent).toBe(true);
      expect(result.count).toBe(3);
    });

    test('should handle zero opportunities', async () => {
      const result = await sendBountyAlert(0, []);
      expect(result.success).toBe(true);
      expect(result.sent).toBe(false);
      expect(result.reason).toBe('No opportunities');
    });

    test('should validate and correct invalid counts', async () => {
      const result = await sendBountyAlert('invalid', []);
      expect(result.success).toBe(true);
      expect(result.sent).toBe(false);
    });
  });
});
