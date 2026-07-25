const { formatBountyAlertTitle, validateCount } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    const validatedCount = validateCount(opportunityCount);
    const title = formatBountyAlertTitle(validatedCount);
    
    const notification = {
      title,
      count: validatedCount,
      opportunities: opportunities.slice(0, validatedCount),
      timestamp: new Date().toISOString()
    };

    console.log(`Sending notification: ${title}`);
    
    // Add your notification delivery logic here
    // e.g., push notification, email, webhook, etc.
    
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
