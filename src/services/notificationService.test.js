const { sendBountyAlert } = require('./notificationService');

describe('sendBountyAlert', () => {
  let mockNotificationClient;
  let mockOpportunities;

  beforeEach(() => {
    mockNotificationClient = {
      send: jest.fn().mockResolvedValue(true)
    };
    
    mockOpportunities = [
      { id: 1, title: 'Bug Bounty 1', reward: 500 },
      { id: 2, title: 'Bug Bounty 2', reward: 1000 },
      { id: 3, title: 'Bug Bounty 3', reward: 750 }
    ];
  });

  test('should send notification with correct title for multiple opportunities', async () => {
    const result = await sendBountyAlert(mockOpportunities, mockNotificationClient);
    
    expect(result).toEqual({ success: true, count: 3 });
    expect(mockNotificationClient.send).toHaveBeenCalledWith(
      expect.objectContaining({
        title: '🎯 Bounty Alert: 3 New Opportunities found',
        body: 'Found 3 new bounty opportunities. Check them out now!',
        data: expect.objectContaining({
          count: 3,
          opportunities: mockOpportunities
        })
      })
    );
  });

  test('should send notification with correct title for single opportunity', async () => {
    const singleOpportunity = [mockOpportunities[0]];
    const result = await sendBountyAlert(singleOpportunity, mockNotificationClient);
    
    expect(result).toEqual({ success: true, count: 1 });
    expect(mockNotificationClient.send).toHaveBeenCalledWith(
      expect.objectContaining({
        title: '🎯 Bounty Alert: 1 New Opportunity found',
        body: 'Found 1 new bounty opportunity. Check them out now!'
      })
    );
  });

  test('should handle empty opportunities array', async () => {
    const result = await sendBountyAlert([], mockNotificationClient);
    
    expect(result).toEqual({ success: true, count: 0 });
    expect(mockNotificationClient.send).toHaveBeenCalledWith(
      expect.objectContaining({
        title: '🎯 Bounty Alert: No new opportunities found',
        body: 'No new bounties at this time.'
      })
    );
  });

  test('should limit opportunities in notification payload to 10', async () => {
    const manyOpportunities = Array.from({ length: 15 }, (_, i) => ({
      id: i + 1,
      title: `Bounty ${i + 1}`,
      reward: 500
    }));
    
    await sendBountyAlert(manyOpportunities, mockNotificationClient);
    
    const callArgs = mockNotificationClient.send.mock.calls[0][0];
    expect(callArgs.data.opportunities).toHaveLength(10);
    expect(callArgs.data.count).toBe(15);
  });

  test('should throw error for invalid opportunities input', async () => {
    await expect(sendBountyAlert('invalid', mockNotificationClient))
      .rejects.toThrow('Opportunities must be an array');
    
    await expect(sendBountyAlert(null, mockNotificationClient))
      .rejects.toThrow('Opportunities must be an array');
  });

  test('should throw error for invalid notification client', async () => {
    await expect(sendBountyAlert(mockOpportunities, null))
      .rejects.toThrow('Valid notification client with send method is required');
    
    await expect(sendBountyAlert(mockOpportunities, {}))
      .rejects.toThrow('Valid notification client with send method is required');
  });

  test('should handle notification client errors', async () => {
    mockNotificationClient.send.mockRejectedValue(new Error('Network error'));
    
    await expect(sendBountyAlert(mockOpportunities, mockNotificationClient))
      .rejects.toThrow('Notification failed: Network error');
  });
});
