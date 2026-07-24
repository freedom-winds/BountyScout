const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    service = new NotificationService();
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('sendBountyAlert', () => {
    test('sends alert for single opportunity', async () => {
      const result = await service.sendBountyAlert(1);
      
      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
      expect(result.notification.count).toBe(1);
      expect(result.notification.timestamp).toBeDefined();
      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[NotificationService] 🎯 Bounty Alert: 1 New Opportunity found'
      );
    });

    test('sends alert for multiple opportunities', async () => {
      const result = await service.sendBountyAlert(13);
      
      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.notification.count).toBe(13);
    });

    test('includes additional options in notification', async () => {
      const options = {
        priority: 'high',
        channel: 'slack'
      };
      const result = await service.sendBountyAlert(5, options);
      
      expect(result.success).toBe(true);
      expect(result.notification.priority).toBe('high');
      expect(result.notification.channel).toBe('slack');
    });

    test('handles invalid count gracefully', async () => {
      const result = await service.sendBountyAlert(-1);
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('Count must be a non-negative number');
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });

  describe('sendBatchBountyAlerts', () => {
    test('sends multiple alerts successfully', async () => {
      const counts = [1, 5, 13];
      const results = await service.sendBatchBountyAlerts(counts);
      
      expect(results).toHaveLength(3);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(true);
      expect(results[2].success).toBe(true);
      expect(results[2].notification.count).toBe(13);
    });

    test('handles mixed valid and invalid counts', async () => {
      const counts = [5, -1, 10];
      const results = await service.sendBatchBountyAlerts(counts);
      
      expect(results).toHaveLength(3);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(false);
      expect(results[2].success).toBe(true);
    });

    test('throws error for non-array input', async () => {
      await expect(service.sendBatchBountyAlerts('not an array'))
        .rejects.toThrow('Counts must be an array');
    });
  });
});
