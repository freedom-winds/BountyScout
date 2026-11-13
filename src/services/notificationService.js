const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    if (typeof count !== 'number' || count < 0) {
      console.error('Invalid count provided to sendBountyNotification');
      return;
    }

    if (count === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const message = formatBountyNotification(count);
    
    // Log the notification
    console.log(message);
    
    // Send notification through configured channels
    await notifyChannels(message, opportunities);
    
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

/**
 * Notifies all configured channels
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyChannels(message, opportunities) {
  const notifications = [];
  
  // Add your notification channels here (Slack, Discord, Email, etc.)
  // Example:
  // if (process.env.SLACK_WEBHOOK_URL) {
  //   notifications.push(sendSlackNotification(message, opportunities));
  // }
  // if (process.env.DISCORD_WEBHOOK_URL) {
  //   notifications.push(sendDiscordNotification(message, opportunities));
  // }
  
  await Promise.allSettled(notifications);
}

module.exports = {
  sendBountyNotification,
  notifyChannels
};
