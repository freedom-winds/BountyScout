const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  describe('sendBountyAlert', () => {
    test('should send notification with correct title for multiple opportunities', async () => {
      const result = await service.sendBountyAlert(15);
      
      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 15 New Opportunities found');
      expect(result.notification.count).toBe(15);
      expect(result.notification.timestamp).toBeDefined();
    });

    test('should send notification with correct title for single opportunity', async () => {
      const result = await service.sendBountyAlert(1);
      
      expect(result.success).toBe(true);
      expect(result.notification.title).toBe('🎯 Bounty Alert: 1 New Opportunity found');
    });

    test('should include additional options in notification', async () => {
      const options = {
        channel: 'slack',
        priority: 'high'
      };
      const result = await service.sendBountyAlert(15, options);
      
      expect(result.success).toBe(true);
      expect(result.notification.channel).toBe('slack');
      expect(result.notification.priority).toBe('high');
    });

    test('should handle errors gracefully', async () => {
      const result = await service.sendBountyAlert('invalid');
      
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('validateOpportunities', () => {
    test('should validate array of opportunities', () => {
      expect(service.validateOpportunities([])).toBe(true);
      expect(service.validateOpportunities([{}, {}])).toBe(true);
    });

    test('should reject non-array input', () => {
      expect(service.validateOpportunities(null)).toBe(false);
      expect(service.validateOpportunities(undefined)).toBe(false);
      expect(service.validateOpportunities('string')).toBe(false);
      expect(service.validateOpportunities(123)).toBe(false);
    });
  });
});
