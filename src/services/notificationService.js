const { formatOpportunityMessage } = require('../utils/notificationFormatter');

/**
 * Send notification about new bounty opportunities
 * @param {number} count - Number of new opportunities found
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    const message = formatOpportunityMessage(count);
    
    // Log the notification
    console.log(message);
    
    // Add your notification logic here (e.g., Slack, Discord, Email, etc.)
    // Example:
    // await sendToSlack(message, opportunities);
    // await sendToDiscord(message, opportunities);
    // await sendEmail(message, opportunities);
    
    return {
      success: true,
      message,
      count
    };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

/**
 * Format opportunities for notification display
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {string} Formatted opportunities list
 */
function formatOpportunitiesList(opportunities) {
  if (!opportunities || opportunities.length === 0) {
    return '';
  }
  
  return opportunities
    .map((opp, index) => {
      const title = opp.title || 'Untitled';
      const reward = opp.reward ? ` - ${opp.reward}` : '';
      const url = opp.url ? ` (${opp.url})` : '';
      return `${index + 1}. ${title}${reward}${url}`;
    })
    .join('\n');
}

module.exports = {
  sendBountyNotification,
  formatOpportunitiesList
};
