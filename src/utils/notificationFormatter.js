/**
 * Formats notification messages for bounty alerts
 * @param {number} count - Number of opportunities found
 * @returns {string} Formatted notification title
 */
function formatBountyAlertTitle(count) {
  if (typeof count !== 'number' || count < 0) {
    throw new Error('Count must be a non-negative number');
  }

  const opportunityText = count === 1 ? 'Opportunity' : 'Opportunities';
  return `🎯 Bounty Alert: ${count} New ${opportunityText} found`;
}

module.exports = {
  formatBountyAlertTitle
};
