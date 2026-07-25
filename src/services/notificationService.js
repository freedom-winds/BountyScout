const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty notifications with proper formatting
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Object} options - Additional notification options
 */
function sendBountyNotification(opportunityCount, options = {}) {
  try {
    const message = formatBountyNotification(opportunityCount);
    
    // Log the notification
    console.log(message);
    
    // Send notification through configured channels
    if (options.channels) {
      options.channels.forEach(channel => {
        channel.send(message);
      });
    }
    
    return {
      success: true,
      message
    };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyNotification
};
