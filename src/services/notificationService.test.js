const { sendBountyNotification, formatOpportunitiesList } = require('./notificationService');
const { formatOpportunityMessage } = require('../utils/notificationFormatter');

jest.mock('../utils/notificationFormatter');

describe('notificationService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    console.log = jest.fn();
    console.error = jest.fn();
  });

  describe('sendBountyNotification', () => {
    test('should send notification with correct message', async () => {
      formatOpportunityMessage.mockReturnValue('🎯 Bounty Alert: 13 New Opportunities found');
      
      const result = await sendBountyNotification(13, []);
      
      expect(formatOpportunityMessage).toHaveBeenCalledWith(13);
      expect(console.log).toHaveBeenCalledWith('🎯 Bounty Alert: 13 New Opportunities found');
      expect(result.success).toBe(true);
      expect(result.count).toBe(13);
    });

    test('should handle errors gracefully', async () => {
      formatOpportunityMessage.mockImplementation(() => {
        throw new Error('Test error');
      });
      
      await expect(sendBountyNotification(5)).rejects.toThrow('Test error');
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('formatOpportunitiesList', () => {
    test('should format opportunities list correctly', () => {
      const opportunities = [
        { title: 'Bug Fix', reward: '$500', url: 'https://example.com/1' },
        { title: 'Feature Request', reward: '$1000', url: 'https://example.com/2' }
      ];
      
      const result = formatOpportunitiesList(opportunities);
      
      expect(result).toContain('1. Bug Fix - $500');
      expect(result).toContain('2. Feature Request - $1000');
    });

    test('should handle empty opportunities array', () => {
      expect(formatOpportunitiesList([])).toBe('');
      expect(formatOpportunitiesList(null)).toBe('');
      expect(formatOpportunitiesList(undefined)).toBe('');
    });

    test('should handle opportunities with missing fields', () => {
      const opportunities = [
        { title: 'Bug Fix' },
        { reward: '$500' },
        {}
      ];
      
      const result = formatOpportunitiesList(opportunities);
      
      expect(result).toContain('1. Bug Fix');
      expect(result).toContain('2. Untitled - $500');
      expect(result).toContain('3. Untitled');
    });
  });
});
