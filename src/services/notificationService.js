const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    if (count === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const message = formatBountyNotification(count);
    
    // Log the notification
    console.log(message);
    
    // Additional notification logic can be added here
    // e.g., sending to Slack, Discord, email, etc.
    
    return message;
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

module.exports = {
  sendBountyNotification
};
