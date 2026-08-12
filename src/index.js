const { formatOpportunityMessage } = require('./utils/notificationFormatter');
const { sendBountyNotification } = require('./services/notificationService');

/**
 * Main function to check for bounties and send notifications
 * @param {Array} opportunities - Array of bounty opportunities
 * @param {Object} config - Configuration options
 * @returns {Promise<void>}
 */
async function checkAndNotify(opportunities = [], config = {}) {
  try {
    const count = Array.isArray(opportunities) ? opportunities.length : 0;
    
    // Only send notification if there are opportunities or if configured to always notify
    if (count > 0 || config.notifyOnZero) {
      await sendBountyNotification(count, config);
    }
    
    return {
      count,
      message: formatOpportunityMessage(count),
      opportunities
    };
  } catch (error) {
    console.error('Error in checkAndNotify:', error);
    throw error;
  }
}

module.exports = {
  checkAndNotify,
  formatOpportunityMessage,
  sendBountyNotification
};
