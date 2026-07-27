const { formatBountyNotification } = require('../utils/notificationFormatter');

/**
 * Sends notifications about new bounty opportunities
 * @param {number} count - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyNotification(count, opportunities = []) {
  try {
    if (!count || count === 0) {
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
 * Sends notifications to all configured channels
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyChannels(message, opportunities) {
  const notificationPromises = [];

  // Add your notification channel implementations here
  // Example: Slack, Discord, Email, etc.
  
  if (process.env.SLACK_WEBHOOK_URL) {
    notificationPromises.push(sendSlackNotification(message, opportunities));
  }
  
  if (process.env.DISCORD_WEBHOOK_URL) {
    notificationPromises.push(sendDiscordNotification(message, opportunities));
  }
  
  if (process.env.EMAIL_ENABLED === 'true') {
    notificationPromises.push(sendEmailNotification(message, opportunities));
  }

  await Promise.allSettled(notificationPromises);
}

/**
 * Sends notification to Slack
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendSlackNotification(message, opportunities) {
  try {
    const fetch = require('node-fetch');
    const webhookUrl = process.env.SLACK_WEBHOOK_URL;
    
    const payload = {
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
    };

    if (opportunities.length > 0) {
      payload.blocks.push({
        type: 'divider'
      });
      
      opportunities.slice(0, 5).forEach(opp => {
        payload.blocks.push({
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*${opp.title || 'Untitled'}*\n${opp.url || ''}`
          }
        });
      });
    }

    const response = await fetch(webhookUrl, {
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
 * Sends notification to Discord
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendDiscordNotification(message, opportunities) {
  try {
    const fetch = require('node-fetch');
    const webhookUrl = process.env.DISCORD_WEBHOOK_URL;
    
    const embeds = [];
    
    if (opportunities.length > 0) {
      opportunities.slice(0, 5).forEach(opp => {
        embeds.push({
          title: opp.title || 'New Opportunity',
          url: opp.url || '',
          description: opp.description || '',
          color: 0x00ff00
        });
      });
    }

    const payload = {
      content: message,
      embeds: embeds
    };

    const response = await fetch(webhookUrl, {
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
 * Sends notification via email
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendEmailNotification(message, opportunities) {
  try {
    // Implement email notification logic here
    console.log('Email notification:', message);
  } catch (error) {
    console.error('Error sending email notification:', error);
  }
}

module.exports = {
  sendBountyNotification,
  notifyChannels
};
