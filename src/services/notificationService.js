const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} notificationClient - Client for sending notifications
 */
async function sendBountyAlert(opportunities, notificationClient) {
  if (!Array.isArray(opportunities)) {
    throw new Error('Opportunities must be an array');
  }

  if (!notificationClient || typeof notificationClient.send !== 'function') {
    throw new Error('Valid notification client with send method is required');
  }

  const count = opportunities.length;
  const title = formatBountyAlertTitle(count);
  
  const message = {
    title,
    body: count > 0 
      ? `Found ${count} new bounty ${count === 1 ? 'opportunity' : 'opportunities'}. Check them out now!`
      : 'No new bounties at this time.',
    data: {
      count,
      opportunities: opportunities.slice(0, 10), // Limit to first 10 for notification payload
      timestamp: new Date().toISOString()
    }
  };

  try {
    await notificationClient.send(message);
    return { success: true, count };
  } catch (error) {
    console.error('Failed to send bounty alert:', error);
    throw new Error(`Notification failed: ${error.message}`);
  }
}

module.exports = {
  sendBountyAlert
};
