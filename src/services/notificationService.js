const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities found
 * @param {Object} options - Notification options
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, options = {}) {
  try {
    const message = formatBountyNotification(opportunityCount);
    
    // Log the notification
    console.log(`[Notification] ${message}`);
    
    // Send notification through configured channels
    const results = [];
    
    if (options.channels) {
      for (const channel of options.channels) {
        try {
          await channel.send(message, options);
          results.push({ channel: channel.name, status: 'success' });
        } catch (error) {
          console.error(`Failed to send notification via ${channel.name}:`, error);
          results.push({ channel: channel.name, status: 'failed', error: error.message });
        }
      }
    }
    
    return {
      success: true,
      message,
      results
    };
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyAlert
};
