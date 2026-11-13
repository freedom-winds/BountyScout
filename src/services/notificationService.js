const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends a bounty alert notification
 * @param {number} count - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @param {Object} options - Notification options
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(count, opportunities = [], options = {}) {
  try {
    if (!Array.isArray(opportunities)) {
      throw new Error('Opportunities must be an array');
    }

    const title = formatBountyAlertTitle(count);
    
    const notification = {
      title,
      timestamp: new Date().toISOString(),
      count,
      opportunities: opportunities.map(opp => ({
        id: opp.id || null,
        title: opp.title || 'Untitled',
        url: opp.url || null,
        reward: opp.reward || null,
        platform: opp.platform || 'Unknown'
      })),
      ...options
    };

    // Log the notification (replace with actual notification service)
    console.log('Bounty Alert:', notification);
    
    return {
      success: true,
      notification
    };
  } catch (error) {
    console.error('Error sending bounty alert:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyAlert
};
