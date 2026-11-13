const NotificationService = require('./notificationService');

describe('NotificationService', () => {
  let service;

  beforeEach(() => {
    service = new NotificationService();
  });

  test('should register notification handlers', () => {
    const handler = jest.fn();
    service.registerHandler(handler);
    expect(service.notificationHandlers).toHaveLength(1);
  });

  test('should throw error when registering non-function handler', () => {
    expect(() => service.registerHandler('not a function')).toThrow('Handler must be a function');
  });

  test('should send bounty alert to all handlers', async () => {
    const handler1 = jest.fn();
    const handler2 = jest.fn();
    
    service.registerHandler(handler1);
    service.registerHandler(handler2);

    await service.sendBountyAlert(12, { source: 'github' });

    expect(handler1).toHaveBeenCalledWith(
      expect.objectContaining({
        message: '🎯 Bounty Alert: 12 New Opportunities found',
        count: 12,
        source: 'github',
        timestamp: expect.any(String)
      })
    );
    expect(handler2).toHaveBeenCalled();
  });

  test('should handle handler failures gracefully', async () => {
    const failingHandler = jest.fn().mockRejectedValue(new Error('Handler failed'));
    const successHandler = jest.fn();
    
    service.registerHandler(failingHandler);
    service.registerHandler(successHandler);

    await service.sendBountyAlert(5);

    expect(failingHandler).toHaveBeenCalled();
    expect(successHandler).toHaveBeenCalled();
  });
});
