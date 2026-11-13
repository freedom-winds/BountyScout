const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} notificationConfig - Configuration for notifications
 */
async function sendBountyAlert(opportunities, notificationConfig = {}) {
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
    const message = formatNotificationMessage(opportunities);
    
    // Send notification through configured channels
    if (notificationConfig.slack) {
      await sendSlackNotification(title, message, notificationConfig.slack);
    }
    
    if (notificationConfig.discord) {
      await sendDiscordNotification(title, message, notificationConfig.discord);
    }
    
    if (notificationConfig.email) {
      await sendEmailNotification(title, message, notificationConfig.email);
    }
    
    console.log(`✅ Sent bounty alert for ${count} opportunities`);
  } catch (error) {
    console.error('Failed to send bounty alert:', error);
    throw error;
  }
}

/**
 * Formats the notification message body
 * @param {Array} opportunities - Array of opportunities
 * @returns {string} Formatted message
 */
function formatNotificationMessage(opportunities) {
  const maxDisplay = 10;
  const displayOpportunities = opportunities.slice(0, maxDisplay);
  
  let message = displayOpportunities.map((opp, index) => {
    return `${index + 1}. ${opp.title || 'Untitled'} - ${opp.reward || 'N/A'} (${opp.platform || 'Unknown'})`;
  }).join('\n');
  
  if (opportunities.length > maxDisplay) {
    message += `\n\n... and ${opportunities.length - maxDisplay} more`;
  }
  
  return message;
}

/**
 * Sends notification to Slack
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 * @param {Object} config - Slack configuration
 */
async function sendSlackNotification(title, message, config) {
  if (!config.webhookUrl) {
    throw new Error('Slack webhook URL is required');
  }
  
  const payload = {
    text: title,
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: title,
          emoji: true
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: message
        }
      }
    ]
  };
  
  const fetch = require('node-fetch');
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
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 * @param {Object} config - Discord configuration
 */
async function sendDiscordNotification(title, message, config) {
  if (!config.webhookUrl) {
    throw new Error('Discord webhook URL is required');
  }
  
  const payload = {
    embeds: [
      {
        title: title,
        description: message,
        color: 3447003,
        timestamp: new Date().toISOString()
      }
    ]
  };
  
  const fetch = require('node-fetch');
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
 * @param {string} title - Notification title
 * @param {string} message - Notification message
 * @param {Object} config - Email configuration
 */
async function sendEmailNotification(title, message, config) {
  if (!config.to || !config.from) {
    throw new Error('Email to and from addresses are required');
  }
  
  // This is a placeholder - implement with your preferred email service
  console.log(`Email notification: ${title}\n${message}`);
}

module.exports = {
  sendBountyAlert,
  formatNotificationMessage
};
