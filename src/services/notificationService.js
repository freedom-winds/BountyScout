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
 * Notifies all configured channels
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function notifyChannels(message, opportunities) {
  const notifications = [];
  
  // Add notification methods as needed
  if (process.env.SLACK_WEBHOOK_URL) {
    notifications.push(sendSlackNotification(message, opportunities));
  }
  
  if (process.env.DISCORD_WEBHOOK_URL) {
    notifications.push(sendDiscordNotification(message, opportunities));
  }
  
  if (process.env.EMAIL_ENABLED === 'true') {
    notifications.push(sendEmailNotification(message, opportunities));
  }
  
  await Promise.allSettled(notifications);
}

/**
 * Sends notification to Slack
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendSlackNotification(message, opportunities) {
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
}

/**
 * Sends notification to Discord
 * @param {string} message - Notification message
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendDiscordNotification(message, opportunities) {
  const fetch = require('node-fetch');
  
  const payload = {
    content: message,
    embeds: opportunities.slice(0, 5).map(opp => ({
      title: opp.title || 'Untitled Opportunity',
      url: opp.url || '',
      description: opp.description || 'No description available',
      color: 3581519,
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
      ]
    }))
  };
  
  const response = await fetch(process.env.DISCORD_WEBHOOK_URL, {
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
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendEmailNotification(message, opportunities) {
  // Placeholder for email notification implementation
  console.log('Email notification:', message);
  // Implement email sending logic based on your email service
}

module.exports = {
  sendBountyNotification,
  notifyChannels,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
