const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} options - Notification options
 */
async function sendBountyAlert(opportunities, options = {}) {
  if (!Array.isArray(opportunities)) {
    throw new Error('Opportunities must be an array');
  }

  const count = opportunities.length;
  
  if (count === 0) {
    console.log('No new opportunities to notify about');
    return;
  }

  try {
    const title = formatBountyAlertTitle(count);
    
    const notification = {
      title,
      opportunities,
      timestamp: new Date().toISOString(),
      ...options
    };

    // Log notification
    console.log(`Sending notification: ${title}`);
    
    // Send notification through configured channels
    await sendNotification(notification);
    
    return notification;
  } catch (error) {
    console.error('Failed to send bounty alert:', error);
    throw error;
  }
}

/**
 * Internal function to send notification through various channels
 * @param {Object} notification - Notification object
 */
async function sendNotification(notification) {
  // Implementation for sending notifications
  // This can be extended to support multiple channels (email, Slack, Discord, etc.)
  return notification;
}

module.exports = {
  sendBountyAlert
};
