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
    throw new Error('Slack webhook URL is required');
  }
  
  const payload = {
    text: message,
    username: config.username || 'BountyScout',
    icon_emoji: config.icon || ':dart:'
  };
  
  const response = await fetch(config.webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) {
    throw new Error(`Slack notification failed: ${response.statusText}`);
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
  
  const payload = {
    content: message,
    username: config.username || 'BountyScout'
  };
  
  const response = await fetch(config.webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) {
    throw new Error(`Discord notification failed: ${response.statusText}`);
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
  // Implement actual email sending logic here
}

module.exports = {
  sendBountyNotification,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
