/**
 * Formats notification messages with proper grammar and spelling
 * @param {number} count - Number of opportunities found
 * @returns {string} Formatted notification message
 */
function formatBountyNotification(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }

  const opportunity = count === 1 ? 'Opportunity' : 'Opportunities';
  const verb = count === 1 ? 'was' : 'were';
  
  return `🎯 Bounty Alert: ${count} New ${opportunity} ${verb} found`;
}

module.exports = {
  formatBountyNotification
};
