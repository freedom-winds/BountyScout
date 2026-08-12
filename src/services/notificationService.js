const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Notification Service
 * Handles sending notifications for bounty alerts
 */
class NotificationService {
  /**
   * Send a bounty alert notification
   * @param {number} count - Number of new opportunities
   * @param {Array} opportunities - Array of opportunity objects
   * @returns {Object} Notification result
   */
  async sendBountyAlert(count, opportunities = []) {
    try {
      if (count === 0) {
        return {
          success: true,
          message: 'No new opportunities to notify'
        };
      }

      const title = formatBountyAlertTitle(count);
      
      const notification = {
        title,
        timestamp: new Date().toISOString(),
        count,
        opportunities: opportunities.slice(0, count)
      };

      // Log the notification
      console.log(`[NotificationService] ${title}`);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('[NotificationService] Error sending bounty alert:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = NotificationService;
