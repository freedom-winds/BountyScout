const { formatOpportunityNotification } = require('../utils/notificationFormatter');

/**
 * Send notification about new bounty opportunities
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} notificationConfig - Configuration for notifications
 * @returns {Promise<void>}
 */
async function sendBountyNotification(opportunities, notificationConfig = {}) {
  try {
    const count = Array.isArray(opportunities) ? opportunities.length : 0;
    const message = formatOpportunityNotification(count);
    
    // Log notification
    console.log(message);
    
    // Send to configured notification channels
    if (notificationConfig.slack && notificationConfig.slack.enabled) {
      await sendSlackNotification(message, opportunities, notificationConfig.slack);
    }
    
    if (notificationConfig.discord && notificationConfig.discord.enabled) {
      await sendDiscordNotification(message, opportunities, notificationConfig.discord);
    }
    
    if (notificationConfig.email && notificationConfig.email.enabled) {
      await sendEmailNotification(message, opportunities, notificationConfig.email);
    }
    
    return { success: true, message, count };
  } catch (error) {
    console.error('Error sending bounty notification:', error);
    throw error;
  }
}

/**
 * Send Slack notification
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunities
 * @param {Object} config - Slack configuration
 */
async function sendSlackNotification(message, opportunities, config) {
  if (!config.webhookUrl) {
    console.warn('Slack webhook URL not configured');
    return;
  }
  
  try {
    const fetch = require('node-fetch');
    const payload = {
      text: message,
      attachments: opportunities.slice(0, 5).map(opp => ({
        title: opp.title || 'Untitled Opportunity',
        title_link: opp.url || '',
        text: opp.description || 'No description available',
        color: '#36a64f',
        fields: [
          {
            title: 'Reward',
            value: opp.reward || 'Not specified',
            short: true
          },
          {
            title: 'Platform',
            value: opp.platform || 'Unknown',
            short: true
          }
        ]
      }))
    };
    
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error(`Slack notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error sending Slack notification:', error);
  }
}

/**
 * Send Discord notification
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunities
 * @param {Object} config - Discord configuration
 */
async function sendDiscordNotification(message, opportunities, config) {
  if (!config.webhookUrl) {
    console.warn('Discord webhook URL not configured');
    return;
  }
  
  try {
    const fetch = require('node-fetch');
    const embeds = opportunities.slice(0, 10).map(opp => ({
      title: opp.title || 'Untitled Opportunity',
      url: opp.url || '',
      description: opp.description || 'No description available',
      color: 3447003,
      fields: [
        {
          name: 'Reward',
          value: opp.reward || 'Not specified',
          inline: true
        },
        {
          name: 'Platform',
          value: opp.platform || 'Unknown',
          inline: true
        }
      ],
      timestamp: new Date().toISOString()
    }));
    
    const payload = {
      content: message,
      embeds: embeds
    };
    
    const response = await fetch(config.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error(`Discord notification failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error sending Discord notification:', error);
  }
}

/**
 * Send Email notification
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunities
 * @param {Object} config - Email configuration
 */
async function sendEmailNotification(message, opportunities, config) {
  console.log('Email notification:', message);
  // Email implementation would go here
  // This is a placeholder for email service integration
}

module.exports = {
  sendBountyNotification,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
