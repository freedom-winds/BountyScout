const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<void>}
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    if (!opportunityCount || opportunityCount === 0) {
      console.log('No new opportunities to notify about');
      return;
    }

    const title = formatBountyAlertTitle(opportunityCount);
    
    const notification = {
      title,
      timestamp: new Date().toISOString(),
      count: opportunityCount,
      opportunities: opportunities.slice(0, 10) // Limit to first 10 for notification
    };

    console.log(`Sending notification: ${title}`);
    
    // Send notification through configured channels
    await notifyChannels(notification);
    
    return notification;
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    throw error;
  }
}

/**
 * Notifies all configured channels
 * @param {Object} notification - Notification object
 * @returns {Promise<void>}
 */
async function notifyChannels(notification) {
  const channels = [];
  
  // Add notification channels based on configuration
  if (process.env.SLACK_WEBHOOK_URL) {
    channels.push(sendSlackNotification(notification));
  }
  
  if (process.env.DISCORD_WEBHOOK_URL) {
    channels.push(sendDiscordNotification(notification));
  }
  
  if (process.env.EMAIL_ENABLED === 'true') {
    channels.push(sendEmailNotification(notification));
  }
  
  if (channels.length === 0) {
    console.log('No notification channels configured');
    return;
  }
  
  await Promise.allSettled(channels);
}

/**
 * Sends notification to Slack
 * @param {Object} notification - Notification object
 * @returns {Promise<void>}
 */
async function sendSlackNotification(notification) {
  const fetch = require('node-fetch');
  
  const payload = {
    text: notification.title,
    blocks: [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: notification.title,
          emoji: true
        }
      },
      {
        type: 'section',
        fields: [
          {
            type: 'mrkdwn',
            text: `*Count:*\n${notification.count}`
          },
          {
            type: 'mrkdwn',
            text: `*Time:*\n${new Date(notification.timestamp).toLocaleString()}`
          }
        ]
      }
    ]
  };
  
  if (notification.opportunities && notification.opportunities.length > 0) {
    const opportunityList = notification.opportunities
      .map(opp => `• ${opp.title || opp.name || 'Untitled'}`)
      .join('\n');
    
    payload.blocks.push({
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: `*Top Opportunities:*\n${opportunityList}`
      }
    });
  }
  
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
 * @param {Object} notification - Notification object
 * @returns {Promise<void>}
 */
async function sendDiscordNotification(notification) {
  const fetch = require('node-fetch');
  
  const embed = {
    title: notification.title,
    color: 0x00ff00,
    timestamp: notification.timestamp,
    fields: [
      {
        name: 'New Opportunities',
        value: notification.count.toString(),
        inline: true
      }
    ]
  };
  
  if (notification.opportunities && notification.opportunities.length > 0) {
    const opportunityList = notification.opportunities
      .slice(0, 5)
      .map(opp => `• ${opp.title || opp.name || 'Untitled'}`)
      .join('\n');
    
    embed.fields.push({
      name: 'Top Opportunities',
      value: opportunityList || 'No details available',
      inline: false
    });
  }
  
  const payload = {
    embeds: [embed]
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
 * @param {Object} notification - Notification object
 * @returns {Promise<void>}
 */
async function sendEmailNotification(notification) {
  // Placeholder for email notification implementation
  console.log('Email notification:', notification.title);
  // Implement email sending logic based on your email service
}

module.exports = {
  sendBountyAlert,
  notifyChannels,
  sendSlackNotification,
  sendDiscordNotification,
  sendEmailNotification
};
