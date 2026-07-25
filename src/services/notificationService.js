const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities found
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
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
    console.error('Error sending bounty notification:', error.message);
    throw error;
  }
}

/**
 * Notifies all configured channels about new opportunities
 * @param {string} message - Formatted notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyChannels(message, opportunities) {
  const notifications = [];
  
  // Add your notification channel implementations here
  // Example: Slack, Discord, Email, etc.
  
  if (process.env.SLACK_WEBHOOK_URL) {
    notifications.push(notifySlack(message, opportunities));
  }
  
  if (process.env.DISCORD_WEBHOOK_URL) {
    notifications.push(notifyDiscord(message, opportunities));
  }
  
  if (process.env.EMAIL_ENABLED === 'true') {
    notifications.push(notifyEmail(message, opportunities));
  }
  
  await Promise.allSettled(notifications);
}

/**
 * Sends notification to Slack
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifySlack(message, opportunities) {
  // Implement Slack notification
  console.log('Slack notification:', message);
}

/**
 * Sends notification to Discord
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyDiscord(message, opportunities) {
  // Implement Discord notification
  console.log('Discord notification:', message);
}

/**
 * Sends notification via Email
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyEmail(message, opportunities) {
  // Implement Email notification
  console.log('Email notification:', message);
}

module.exports = {
  sendBountyNotification,
  notifyChannels
};
