const { formatOpportunityNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities found
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    if (count === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const message = formatOpportunityNotification(count);
    console.log(message);
    
    // Log opportunity details if available
    if (opportunities.length > 0) {
      console.log('\nOpportunity Details:');
      opportunities.forEach((opp, index) => {
        console.log(`${index + 1}. ${opp.title || 'Untitled'} - ${opp.reward || 'N/A'}`);
      });
    }
    
    // Additional notification channels can be added here
    // e.g., Discord, Slack, Email, etc.
    
    return message;
  } catch (error) {
    console.error('Error sending bounty notification:', error.message);
    throw error;
  }
}

module.exports = {
  sendBountyNotification
};
