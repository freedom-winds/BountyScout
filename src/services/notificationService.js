const { formatBountyAlert } = require('../utils/notificationFormatter');

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
      const message = formatBountyAlert(opportunityCount);
      
      const notification = {
        title: message,
        timestamp: new Date().toISOString(),
        count: opportunityCount,
        ...options
      };

      // Log the notification
      console.log(`[NotificationService] ${message}`);
      
      return {
        success: true,
        notification
      };
    } catch (error) {
      console.error('[NotificationService] Error sending bounty alert:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Sends batch bounty alerts
   * @param {Array<number>} counts - Array of opportunity counts
   * @returns {Promise<Array<Object>>} Array of notification results
   */
  async sendBatchBountyAlerts(counts) {
    if (!Array.isArray(counts)) {
      throw new Error('Counts must be an array');
    }

    const results = [];
    for (const count of counts) {
      const result = await this.sendBountyAlert(count);
      results.push(result);
    }
    
    return results;
  }
}

module.exports = NotificationService;
