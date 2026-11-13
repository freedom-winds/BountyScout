/**
 * Formats notification messages with proper grammar
 * @param {number} count - Number of opportunities
 * @returns {string} Formatted notification message
 */
function formatOpportunityMessage(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }
  
  const opportunityWord = count === 1 ? 'Opportunity' : 'Opportunities';
  const verb = count === 1 ? 'found' : 'found';
  
  return `🎯 Bounty Alert: ${count} New ${opportunityWord} ${verb}`;
}

module.exports = {
  formatOpportunityMessage
};
