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
    if (options.slack && options.slackWebhook) {
      await sendSlackNotification(options.slackWebhook, message, count);
    }
    
    if (options.discord && options.discordWebhook) {
      await sendDiscordNotification(options.discordWebhook, message, count);
    }
    
    if (options.email && options.emailConfig) {
      await sendEmailNotification(options.emailConfig, message, count);
    }
    
    return { success: true, message };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

/**
 * Sends notification to Slack
 * @param {string} webhook - Slack webhook URL
 * @param {string} message - Notification message
 * @param {number} count - Number of opportunities
 * @returns {Promise<void>}
 */
async function sendSlackNotification(webhook, message, count) {
  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: message,
        blocks: [
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: message
            }
          }
        ]
      })
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
 * @param {string} webhook - Discord webhook URL
 * @param {string} message - Notification message
 * @param {number} count - Number of opportunities
 * @returns {Promise<void>}
 */
async function sendDiscordNotification(webhook, message, count) {
  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        content: message,
        embeds: [
          {
            title: '🎯 Bounty Alert',
            description: `Found ${count} new ${count === 1 ? 'opportunity' : 'opportunities'}`,
            color: 0x00ff00,
            timestamp: new Date().toISOString()
          }
        ]
      })
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
 * Sends notification via email
 * @param {Object} config - Email configuration
 * @param {string} message - Notification message
 * @param {number} count - Number of opportunities
 * @returns {Promise<void>}
 */
async function sendEmailNotification(config, message, count) {
  try {
    // Email implementation would depend on the email service being used
    // This is a placeholder for the actual implementation
    console.log(`Email notification: ${message}`);
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
