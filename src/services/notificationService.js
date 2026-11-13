const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  /**
   * Sends a bounty alert notification
   * @param {number} opportunityCount - Number of new opportunities found
   * @param {Object} options - Additional notification options
   * @returns {Promise<Object>} Notification result
   */
  async sendBountyAlert(opportunityCount, options = {}) {
    try {
      const title = formatBountyAlertTitle(opportunityCount);
      
      const notification = {
        title,
        timestamp: new Date().toISOString(),
        count: opportunityCount,
        ...options
      };

      // Log the notification (can be extended to send to various channels)
      console.log('Sending notification:', notification);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('Failed to send bounty alert:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Validates opportunity data before sending notification
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {boolean} Whether the data is valid
   */
  validateOpportunities(opportunities) {
    if (!Array.isArray(opportunities)) {
      return false;
    }
    return opportunities.length >= 0;
  }
}

module.exports = NotificationService;
