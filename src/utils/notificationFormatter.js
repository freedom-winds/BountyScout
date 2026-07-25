/**
 * Format notification messages with proper grammar
 * @param {number} count - Number of opportunities
 * @returns {string} Formatted notification message
 */
function formatOpportunityNotification(count) {
  if (count === 0) {
    return '🎯 Bounty Alert: No new opportunities found';
  } else if (count === 1) {
    return '🎯 Bounty Alert: 1 New Opportunity found';
  } else {
    return `🎯 Bounty Alert: ${count} New Opportunities found`;
  }
}

module.exports = {
  formatOpportunityNotification
};
