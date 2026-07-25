/**
 * Formats notification messages with proper grammar
 * @param {number} count - Number of opportunities
 * @returns {string} Formatted notification message
 */
function formatOpportunityMessage(count) {
  if (count === 0) {
    return '🎯 Bounty Alert: No new opportunities found';
  }
  
  if (count === 1) {
    return '🎯 Bounty Alert: 1 New Opportunity found';
  }
  
  return `🎯 Bounty Alert: ${count} New Opportunities found`;
}

module.exports = {
  formatOpportunityMessage
};
