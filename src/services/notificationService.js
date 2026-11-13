const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} notificationConfig - Configuration for notifications
 */
async function sendBountyAlert(opportunities, notificationConfig = {}) {
  if (!Array.isArray(opportunities)) {
    throw new Error('Opportunities must be an array');
  }

  const count = opportunities.length;
  
  if (count === 0) {
    console.log('No new opportunities to notify about');
    return;
  }

  const title = formatBountyAlertTitle(count);
  
  const notification = {
    title,
    opportunities,
    timestamp: new Date().toISOString(),
    ...notificationConfig
  };

  // Log notification
  console.log(`Sending notification: ${title}`);
  
  return notification;
}

module.exports = {
  sendBountyAlert
};
