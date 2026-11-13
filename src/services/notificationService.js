const { formatBountyAlertTitle, validateOpportunityCount } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {number} opportunityCount - Number of new opportunities
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {Promise<Object>} Notification result
 */
async function sendBountyAlert(opportunityCount, opportunities = []) {
  try {
    const validatedCount = validateOpportunityCount(opportunityCount);
    
    if (validatedCount === 0) {
      console.log('No new opportunities to notify about');
      return { success: true, sent: false, reason: 'No opportunities' };
    }

    const title = formatBountyAlertTitle(validatedCount);
    const message = formatNotificationMessage(opportunities);

    // Send notification through configured channels
    await sendNotification({
      title,
      message,
      count: validatedCount,
      timestamp: new Date().toISOString()
    });

    console.log(`Notification sent: ${title}`);
    return { success: true, sent: true, count: validatedCount };
  } catch (error) {
    console.error('Error sending bounty alert:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Formats the notification message body
 * @param {Array} opportunities - Array of opportunity objects
 * @returns {string} Formatted message
 */
function formatNotificationMessage(opportunities) {
  if (!Array.isArray(opportunities) || opportunities.length === 0) {
    return 'New bounty opportunities are available!';
  }

  const preview = opportunities.slice(0, 3).map((opp, index) => {
    const title = opp.title || 'Untitled';
    const reward = opp.reward ? ` - ${opp.reward}` : '';
    return `${index + 1}. ${title}${reward}`;
  }).join('\n');

  const remaining = opportunities.length > 3 ? `\n...and ${opportunities.length - 3} more` : '';
  return `${preview}${remaining}`;
}

/**
 * Sends notification through configured channels
 * @param {Object} notification - Notification data
 * @returns {Promise<void>}
 */
async function sendNotification(notification) {
  // Implementation depends on notification channels (Slack, Discord, Email, etc.)
  // This is a placeholder that can be extended based on configuration
  
  const notificationChannels = process.env.NOTIFICATION_CHANNELS?.split(',') || ['console'];
  
  for (const channel of notificationChannels) {
    switch (channel.trim().toLowerCase()) {
      case 'console':
        console.log('📢 Notification:', notification);
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
 * @param {Object} notification - Notification data
 * @returns {Promise<void>}
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
    console.error('Error sending Slack notification:', error);
  }
}

/**
 * Sends notification to Discord
 * @param {Object} notification - Notification data
 * @returns {Promise<void>}
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
        content: notification.title,
        embeds: [
          {
            title: notification.title,
            description: notification.message,
            color: 0x00ff00,
            timestamp: notification.timestamp
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Discord API error: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error sending Discord notification:', error);
  }
}

/**
 * Sends notification via email
 * @param {Object} notification - Notification data
 * @returns {Promise<void>}
 */
async function sendEmailNotification(notification) {
  // Email implementation would go here
  // Requires email service configuration (SendGrid, AWS SES, etc.)
  console.log('Email notification:', notification);
}

module.exports = {
  sendBountyAlert,
  formatNotificationMessage
};
