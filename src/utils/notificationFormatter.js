/**
 * Format notification messages with proper grammar
 * @param {number} count - Number of opportunities
 * @returns {string} Formatted message
 */
function formatOpportunityMessage(count) {
  if (count === 0) {
    return 'No new opportunities found';
  }
  
  const opportunityText = count === 1 ? 'Opportunity' : 'Opportunities';
  return `🎯 Bounty Alert: ${count} New ${opportunityText} found`;
}

module.exports = {
  formatOpportunityMessage
};
