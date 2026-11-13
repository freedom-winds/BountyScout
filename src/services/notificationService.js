const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} options - Notification options
 */
async function sendBountyAlert(opportunities, options = {}) {
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
    await sendNotification({
      title,
      message,
      ...options
    });

    console.log(`Notification sent: ${title}`);
  } catch (error) {
    console.error('Failed to send bounty alert:', error.message);
    throw error;
  }
}

/**
 * Formats the notification message body
 * @param {Array} opportunities - Array of opportunities
 * @returns {string} Formatted message
 */
function formatNotificationMessage(opportunities) {
  if (!opportunities || opportunities.length === 0) {
    return 'No opportunities available';
  }

  const maxDisplay = 5;
  const displayOpportunities = opportunities.slice(0, maxDisplay);
  
  let message = displayOpportunities.map((opp, index) => {
    const title = opp.title || 'Untitled';
    const reward = opp.reward ? ` - ${opp.reward}` : '';
    const platform = opp.platform ? ` (${opp.platform})` : '';
    return `${index + 1}. ${title}${reward}${platform}`;
  }).join('\n');

  if (opportunities.length > maxDisplay) {
    message += `\n\n...and ${opportunities.length - maxDisplay} more`;
  }

  return message;
}

/**
 * Sends notification through configured channels
 * @param {Object} notification - Notification object
 */
async function sendNotification(notification) {
  // Implementation depends on notification channels (Slack, Discord, Email, etc.)
  // This is a placeholder that can be extended based on the app's requirements
  
  const channels = process.env.NOTIFICATION_CHANNELS?.split(',') || ['console'];
  
  for (const channel of channels) {
    switch (channel.trim().toLowerCase()) {
      case 'console':
        console.log('='.repeat(50));
        console.log(notification.title);
        console.log('-'.repeat(50));
        console.log(notification.message);
        console.log('='.repeat(50));
        break;
      
      case 'slack':
        await sendSlackNotification(notification);
        break;
      
      case 'discord':
        await sendDiscordNotification(notification);
        break;
      
      case 'email':
        await sendEmailNotification(notification);
        break;
      
      default:
        console.warn(`Unknown notification channel: ${channel}`);
    }
  }
}

/**
 * Sends notification to Slack
 * @param {Object} notification - Notification object
 */
async function sendSlackNotification(notification) {
  const webhookUrl = process.env.SLACK_WEBHOOK_URL;
  
  if (!webhookUrl) {
    console.warn('Slack webhook URL not configured');
    return;
  }

  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: notification.title,
        blocks: [
          {
            type: 'header',
            text: {
              type: 'plain_text',
              text: notification.title
            }
          },
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: notification.message
            }
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Slack API error: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Failed to send Slack notification:', error.message);
  }
}

/**
 * Sends notification to Discord
 * @param {Object} notification - Notification object
 */
async function sendDiscordNotification(notification) {
  const webhookUrl = process.env.DISCORD_WEBHOOK_URL;
  
  if (!webhookUrl) {
    console.warn('Discord webhook URL not configured');
    return;
  }

  try {
    const fetch = require('node-fetch');
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        embeds: [
          {
            title: notification.title,
            description: notification.message,
            color: 0x00ff00,
            timestamp: new Date().toISOString()
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Discord API error: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Failed to send Discord notification:', error.message);
  }
}

/**
 * Sends notification via email
 * @param {Object} notification - Notification object
 */
async function sendEmailNotification(notification) {
  // Email implementation would go here
  // This is a placeholder for email service integration
  console.log('Email notification:', notification.title);
}

module.exports = {
  sendBountyAlert,
  formatNotificationMessage,
  sendNotification
};
