const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Object} Notification result
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    if (typeof opportunityCount !== 'number' || opportunityCount < 0) {
      throw new Error('Invalid opportunity count');
    }

    if (!Array.isArray(opportunities)) {
      throw new Error('Opportunities must be an array');
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    const notification = {
      title,
      count: opportunityCount,
      opportunities: opportunities.slice(0, opportunityCount),
      timestamp: new Date().toISOString()
    };

    // Log the notification
    console.log(`[BountyScout] ${title}`);
    
    return {
      success: true,
      notification
    };
  } catch (error) {
    console.error('[BountyScout] Error sending bounty alert:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyAlert
};
