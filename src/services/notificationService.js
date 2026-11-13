const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty notifications with properly formatted messages
 */
class NotificationService {
  /**
   * Send a bounty alert notification
   * @param {number} count - Number of new opportunities
   * @param {Object} options - Additional notification options
   * @returns {Promise<void>}
   */
  async sendBountyAlert(count, options = {}) {
    try {
      const message = formatBountyNotification(count);
      
      // Send notification through configured channels
      await this.sendNotification({
        title: message,
        ...options
      });
      
      console.log(`Notification sent: ${message}`);
    } catch (error) {
      console.error('Failed to send bounty alert:', error);
      throw error;
    }
  }

  /**
   * Internal method to send notifications
   * @param {Object} notification - Notification payload
   * @returns {Promise<void>}
   */
  async sendNotification(notification) {
    // Implementation depends on notification channel (Slack, Discord, Email, etc.)
    // This is a placeholder that should be implemented based on the app's needs
    return Promise.resolve();
  }
}

module.exports = NotificationService;
