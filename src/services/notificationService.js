const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Notification service for sending bounty alerts
 */
class NotificationService {
  constructor(config = {}) {
    this.config = config;
    this.notificationHandlers = [];
  }

  /**
   * Register a notification handler
   * @param {Function} handler - Function to handle notifications
   */
  registerHandler(handler) {
    if (typeof handler !== 'function') {
      throw new Error('Handler must be a function');
    }
    this.notificationHandlers.push(handler);
  }

  /**
   * Send bounty alert notification
   * @param {number} count - Number of new opportunities
   * @param {Object} metadata - Additional metadata about opportunities
   * @returns {Promise<void>}
   */
  async sendBountyAlert(count, metadata = {}) {
    try {
      const message = formatBountyNotification(count);
      const notification = {
        message,
        count,
        timestamp: new Date().toISOString(),
        ...metadata
      };

      const promises = this.notificationHandlers.map(handler => 
        Promise.resolve(handler(notification)).catch(err => {
          console.error('Notification handler failed:', err);
          return null;
        })
      );

      await Promise.all(promises);
    } catch (error) {
      console.error('Failed to send bounty alert:', error);
      throw error;
    }
  }
}

module.exports = NotificationService;
