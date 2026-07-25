const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends a bounty alert notification
 * @param {number} opportunityCount - Number of new opportunities found
 * @param {Array} opportunities - Array of opportunity objects
 * @param {Object} notificationClient - Client for sending notifications
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, opportunities = [], notificationClient) {
  try {
    if (!notificationClient) {
      throw new Error('Notification client is required');
    }

    if (!Array.isArray(opportunities)) {
      throw new Error('Opportunities must be an array');
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    const message = opportunities.length > 0
      ? opportunities.map((opp, index) => 
          `${index + 1}. ${opp.title || 'Untitled'} - ${opp.reward || 'N/A'}`
        ).join('\n')
      : 'Check the dashboard for details.';

    const notification = {
      title,
      message,
      timestamp: new Date().toISOString(),
      count: opportunityCount,
      opportunities
    };

    const result = await notificationClient.send(notification);
    
    return {
      success: true,
      notification,
      result
    };
  } catch (error) {
    console.error('Failed to send bounty alert:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendBountyAlert
};
