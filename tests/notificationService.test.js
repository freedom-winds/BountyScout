const { sendBountyNotification } = require('../src/services/notificationService');
const { formatBountyNotification } = require('../src/utils/notificationFormatter');

jest.mock('../src/utils/notificationFormatter');

describe('sendBountyNotification', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  test('should send notification with correct message', async () => {
    formatBountyNotification.mockReturnValue('🎯 Bounty Alert: 12 New Opportunities found');
    
    const result = await sendBountyNotification(12);
    
    expect(formatBountyNotification).toHaveBeenCalledWith(12);
    expect(result.success).toBe(true);
    expect(result.message).toBe('🎯 Bounty Alert: 12 New Opportunities found');
  });

  test('should send notification through multiple channels', async () => {
    formatBountyNotification.mockReturnValue('🎯 Bounty Alert: 5 New Opportunities found');
    
    const mockChannel1 = {
      name: 'email',
      send: jest.fn().mockResolvedValue({ sent: true })
    };
    
    const mockChannel2 = {
      name: 'slack',
      send: jest.fn().mockResolvedValue({ sent: true })
    };
    
    const result = await sendBountyNotification(5, {
      channels: [mockChannel1, mockChannel2]
    });
    
    expect(result.success).toBe(true);
    expect(result.results).toHaveLength(2);
    expect(result.results[0].success).toBe(true);
    expect(result.results[1].success).toBe(true);
  });

  test('should handle channel failures gracefully', async () => {
    formatBountyNotification.mockReturnValue('🎯 Bounty Alert: 3 New Opportunities found');
    
    const mockChannel = {
      name: 'failing-channel',
      send: jest.fn().mockRejectedValue(new Error('Channel error'))
    };
    
    const result = await sendBountyNotification(3, {
      channels: [mockChannel]
    });
    
    expect(result.success).toBe(true);
    expect(result.results[0].success).toBe(false);
    expect(result.results[0].error).toBe('Channel error');
  });

  test('should throw error when formatting fails', async () => {
    formatBountyNotification.mockImplementation(() => {
      throw new Error('Formatting error');
    });
    
    await expect(sendBountyNotification(-1)).rejects.toThrow('Formatting error');
  });
});
