/**
 * Formats notification messages for bounty alerts
 * @param {number} count - Number of opportunities found
 * @returns {string} Formatted notification title
 */
function formatBountyAlertTitle(count) {
  if (typeof count !== 'number' || isNaN(count) || count < 0) {
    throw new Error('Count must be a valid non-negative number');
  }

  const pluralSuffix = count === 1 ? 'y' : 'ies';
  return `🎯 Bounty Alert: ${count} New Opportunit${pluralSuffix} found`;
}

module.exports = {
  formatBountyAlertTitle
};
