const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    if (!opportunityCount || opportunityCount === 0) {
      console.log('No new opportunities to notify about');
      return { success: true, message: 'No notifications sent' };
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    const notification = {
      title,
      timestamp: new Date().toISOString(),
      count: opportunityCount,
      opportunities: opportunities.slice(0, 10) // Limit to first 10 for notification
    };

    console.log(`Notification: ${title}`);
    
    // Here you would integrate with your notification system
    // e.g., Discord, Slack, Email, etc.
    
    return {
      success: true,
      notification
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
