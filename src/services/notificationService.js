const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} count - Number of new opportunities found
 * @param {Object} options - Notification options
 * @returns {Promise<void>}
 */
async function sendBountyAlert(count, options = {}) {
  try {
    const message = formatBountyNotification(count);
    
    // Log the notification
    console.log(message);
    
    // Send to configured notification channels
    if (options.slack) {
      await sendSlackNotification(message, options.slack);
    }
    
    if (options.discord) {
      await sendDiscordNotification(message, options.discord);
    }
    
    if (options.email) {
      await sendEmailNotification(message, options.email);
    }
    
    return message;
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    throw error;
  }
}

/**
 * Sends notification to Slack
 * @param {string} message - Notification message
 * @param {Object} config - Slack configuration
 */
async function sendSlackNotification(message, config) {
  if (!config.webhookUrl) {
    throw new Error('Slack webhook URL is required');
  }
  
  try {
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: message,
        username: config.username || 'BountyScout',
        icon_emoji: config.icon || ':dart:'
      })
    });
    
    if (!response.ok) {
      throw new Error(`Slack notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Failed to send Slack notification:', error);
    throw error;
  }
}

/**
 * Sends notification to Discord
 * @param {string} message - Notification message
 * @param {Object} config - Discord configuration
 */
async function sendDiscordNotification(message, config) {
  if (!config.webhookUrl) {
    throw new Error('Discord webhook URL is required');
  }
  
  try {
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: message,
        username: config.username || 'BountyScout'
      })
    });
    
    if (!response.ok) {
      throw new Error(`Discord notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Failed to send Discord notification:', error);
    throw error;
  }
}

/**
 * Sends email notification
 * @param {string} message - Notification message
 * @param {Object} config - Email configuration
 */
async function sendEmailNotification(message, config) {
  if (!config.to) {
    throw new Error('Email recipient is required');
  }
  
  // This would integrate with your email service (SendGrid, AWS SES, etc.)
  console.log(`Email notification would be sent to ${config.to}: ${message}`);
}

module.exports = {
  sendBountyAlert,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
