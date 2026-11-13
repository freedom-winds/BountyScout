const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    if (!opportunityCount || opportunityCount === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    // Log the notification (can be extended to send to various channels)
    console.log(title);
    
    if (opportunities.length > 0) {
      console.log('Opportunities:', opportunities.map(o => o.title || o.name).join(', '));
    }

    // Add your notification logic here (e.g., Discord, Slack, Email, etc.)
    // await sendToDiscord(title, opportunities);
    // await sendToSlack(title, opportunities);
    
    return { success: true, title, count: opportunityCount };
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    throw error;
  }
}

module.exports = {
  sendBountyAlert
};
