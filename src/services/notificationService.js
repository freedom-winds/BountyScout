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
    
    const response = await fetch(process.env.SLACK_WEBHOOK_URL, {
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
    
    const response = await fetch(process.env.DISCORD_WEBHOOK_URL, {
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
  notifyChannels,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
