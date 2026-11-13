const { sendBountyNotification } = require('./notificationService');
const { formatBountyNotification } = require('../utils/notificationFormatter');

jest.mock('../utils/notificationFormatter');

describe('sendBountyNotification', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  test('sends notification with correct message', async () => {
    formatBountyNotification.mockReturnValue('🎯 Bounty Alert: 15 New Opportunities found');
    
    const result = await sendBountyNotification(15, []);
    
    expect(formatBountyNotification).toHaveBeenCalledWith(15);
    expect(console.log).toHaveBeenCalledWith('🎯 Bounty Alert: 15 New Opportunities found');
    expect(result.success).toBe(true);
    expect(result.count).toBe(15);
  });

  test('handles invalid count gracefully', async () => {
    const result = await sendBountyNotification(-1, []);
    
    expect(console.error).toHaveBeenCalledWith('Invalid count provided to sendBountyNotification');
    expect(result).toBeUndefined();
  });

  test('handles invalid opportunities array', async () => {
    const result = await sendBountyNotification(15, 'not an array');
    
    expect(console.error).toHaveBeenCalledWith('Opportunities must be an array');
    expect(result).toBeUndefined();
  });

  test('handles errors from formatter', async () => {
    formatBountyNotification.mockImplementation(() => {
      throw new Error('Formatter error');
    });
    
    await expect(sendBountyNotification(15, [])).rejects.toThrow('Formatter error');
    expect(console.error).toHaveBeenCalled();
  });
});
