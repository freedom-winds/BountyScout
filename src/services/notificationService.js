const { formatOpportunityMessage } = require('../utils/notificationFormatter');

/**
 * Sends notification about new bounty opportunities
 * @param {number} count - Number of new opportunities
 * @param {Object} options - Notification options
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, options = {}) {
  try {
    const message = formatOpportunityMessage(count);
    
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
    
    return { success: true, message };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
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
    console.warn('Slack webhook URL not configured');
    return;
  }
  
  try {
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: message,
        username: config.username || 'BountyScout',
        icon_emoji: config.icon || ':dart:',
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Slack notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error sending Slack notification:', error);
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
    console.warn('Discord webhook URL not configured');
    return;
  }
  
  try {
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: message,
        username: config.username || 'BountyScout',
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Discord notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error sending Discord notification:', error);
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
    console.warn('Email recipient not configured');
    return;
  }
  
  console.log(`Email notification would be sent to ${config.to}: ${message}`);
  // Email implementation would go here
}

module.exports = {
  sendBountyNotification,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification,
};
