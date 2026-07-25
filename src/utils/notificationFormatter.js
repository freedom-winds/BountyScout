/**
 * Formats notification messages with proper grammar and spelling
 * @param {number} count - Number of opportunities found
 * @returns {string} Formatted notification message
 */
function formatBountyNotification(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }
  
  const opportunityText = count === 1 ? 'Opportunity' : 'Opportunities';
  const foundText = count === 1 ? 'found' : 'found';
  
  return `🎯 Bounty Alert: ${count} New ${opportunityText} ${foundText}`;
}

module.exports = {
  formatBountyNotification
};
