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

/**
 * Validates and sanitizes opportunity count
 * @param {*} count - Raw count value
 * @returns {number} Validated count
 */
function validateOpportunityCount(count) {
  const parsed = parseInt(count, 10);
  if (isNaN(parsed) || parsed < 0) {
    return 0;
  }
  return parsed;
}

module.exports = {
  formatBountyAlertTitle,
  validateOpportunityCount
};
