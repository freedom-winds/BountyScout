const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty notifications with proper formatting
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Object} options - Notification options
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyNotification(opportunityCount, options = {}) {
  try {
    const message = formatBountyNotification(opportunityCount);
    
    // Log the notification
    console.log(`[${new Date().toISOString()}] ${message}`);
    
    // Send notification through configured channels
    const results = [];
    
    if (options.channels) {
      for (const channel of options.channels) {
        try {
          const result = await channel.send(message, options);
          results.push({ channel: channel.name, success: true, result });
        } catch (error) {
          console.error(`Failed to send notification via ${channel.name}:`, error);
          results.push({ channel: channel.name, success: false, error: error.message });
        }
      }
    }
    
    return {
      success: true,
      message,
      results
    };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

module.exports = {
  sendBountyNotification
};
