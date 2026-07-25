const NotificationService = require('../src/services/notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
    service.sendNotification = jest.fn().mockResolvedValue();
  });

  test('sends notification with correct message for singular opportunity', async () => {
    await service.sendBountyAlert(1);
    
    expect(service.sendNotification).toHaveBeenCalledWith({
      title: '🎯 Bounty Alert: 1 New Opportunity was Found'
    });
  });

  test('sends notification with correct message for plural opportunities', async () => {
    await service.sendBountyAlert(15);
    
    expect(service.sendNotification).toHaveBeenCalledWith({
      title: '🎯 Bounty Alert: 15 New Opportunities were Found'
    });
  });

  test('includes additional options in notification', async () => {
    const options = {
      priority: 'high',
      channel: 'bounties'
    };
    
    await service.sendBountyAlert(5, options);
    
    expect(service.sendNotification).toHaveBeenCalledWith({
      title: '🎯 Bounty Alert: 5 New Opportunities were Found',
      priority: 'high',
      channel: 'bounties'
    });
  });

  test('handles notification errors gracefully', async () => {
    const error = new Error('Network error');
    service.sendNotification = jest.fn().mockRejectedValue(error);
    
    await expect(service.sendBountyAlert(10)).rejects.toThrow('Network error');
  });

  test('logs successful notification', async () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    
    await service.sendBountyAlert(3);
    
    expect(consoleSpy).toHaveBeenCalledWith(
      'Notification sent: 🎯 Bounty Alert: 3 New Opportunities were Found'
    );
    
    consoleSpy.mockRestore();
  });

  test('logs errors when notification fails', async () => {
    const error = new Error('Failed to send');
    service.sendNotification = jest.fn().mockRejectedValue(error);
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    await expect(service.sendBountyAlert(5)).rejects.toThrow();
    
    expect(consoleSpy).toHaveBeenCalledWith('Failed to send bounty alert:', error);
    
    consoleSpy.mockRestore();
  });
});
