/**
 * Formats notification messages with proper grammar
 * @param {number} count - Number of opportunities
 * @returns {string} Formatted notification message
 */
function formatOpportunityNotification(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }
  
  const opportunityWord = count === 1 ? 'Opportunity' : 'Opportunities';
  const verb = count === 1 ? 'was' : 'were';
  
  return `🎯 Bounty Alert: ${count} New ${opportunityWord} ${verb} found`;
}

module.exports = {
  formatOpportunityNotification
};
