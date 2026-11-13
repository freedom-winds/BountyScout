const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    if (typeof count !== 'number' || count < 0) {
      console.error('Invalid count provided to sendBountyNotification');
      return;
    }

    if (!Array.isArray(opportunities)) {
      console.error('Opportunities must be an array');
      return;
    }

    const message = formatBountyNotification(count);
    
    // Log the notification
    console.log(message);
    
    // Additional notification logic can be added here
    // e.g., sending to Slack, Discord, email, etc.
    
    return {
      success: true,
      message,
      count,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

module.exports = {
  sendBountyNotification
};
