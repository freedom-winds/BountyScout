const { formatOpportunityMessage } = require('../utils/notificationFormatter');

/**
 * Send notification about new bounty opportunities
 * @param {number} count - Number of new opportunities found
 * @param {Object} options - Notification options
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, options = {}) {
  try {
    const message = formatOpportunityMessage(count);
    
    // Log notification
    console.log(message);
    
    // Send to configured notification channels
    if (options.slack && options.slackWebhook) {
      await sendSlackNotification(message, options.slackWebhook);
    }
    
    if (options.discord && options.discordWebhook) {
      await sendDiscordNotification(message, options.discordWebhook);
    }
    
    if (options.email && options.emailConfig) {
      await sendEmailNotification(message, options.emailConfig);
    }
    
    return message;
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

/**
 * Send notification to Slack
 * @param {string} message - Notification message
 * @param {string} webhookUrl - Slack webhook URL
 * @returns {Promise<void>}
 */
async function sendSlackNotification(message, webhookUrl) {
  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: message })
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
 * Send notification to Discord
 * @param {string} message - Notification message
 * @param {string} webhookUrl - Discord webhook URL
 * @returns {Promise<void>}
 */
async function sendDiscordNotification(message, webhookUrl) {
  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: message })
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
 * Send email notification
 * @param {string} message - Notification message
 * @param {Object} emailConfig - Email configuration
 * @returns {Promise<void>}
 */
async function sendEmailNotification(message, emailConfig) {
  try {
    // Placeholder for email implementation
    // This would typically use nodemailer or similar
    console.log('Email notification:', message);
  } catch (error) {
    console.error('Error sending email notification:', error);
    throw error;
  }
}

module.exports = {
  sendBountyNotification,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
