const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    if (opportunityCount === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    // Log the notification
    console.log(title);
    
    // Additional notification logic can be added here
    // (e.g., sending to Slack, Discord, email, etc.)
    
    return {
      success: true,
      title,
      count: opportunityCount,
      opportunities
    };
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    throw error;
  }
}

module.exports = {
  sendBountyAlert
};
