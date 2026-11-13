const { formatBountyAlertTitle } = require('../utils/notificationFormatter');

/**
 * Sends bounty alert notifications
 * @param {Array} opportunities - Array of new opportunities
 * @param {Object} config - Notification configuration
 */
async function sendBountyAlert(opportunities, config = {}) {
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
    const message = {
      title,
      count,
      opportunities: opportunities.map(opp => ({
        id: opp.id,
        title: opp.title,
        reward: opp.reward,
        url: opp.url,
        platform: opp.platform
      })),
      timestamp: new Date().toISOString()
    };

    // Send notification through configured channels
    if (config.webhook) {
      await sendWebhookNotification(config.webhook, message);
    }
    
    if (config.email) {
      await sendEmailNotification(config.email, message);
    }

    if (config.slack) {
      await sendSlackNotification(config.slack, message);
    }

    console.log(`✅ ${title}`);
    return message;
  } catch (error) {
    console.error('Failed to send bounty alert:', error.message);
    throw error;
  }
}

/**
 * Sends notification via webhook
 */
async function sendWebhookNotification(webhookUrl, message) {
  const fetch = require('node-fetch');
  
  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message)
    });

    if (!response.ok) {
      throw new Error(`Webhook request failed with status ${response.status}`);
    }
  } catch (error) {
    console.error('Webhook notification failed:', error.message);
    throw error;
  }
}

/**
 * Sends notification via email
 */
async function sendEmailNotification(emailConfig, message) {
  // Placeholder for email notification implementation
  console.log('Email notification:', message.title);
}

/**
 * Sends notification via Slack
 */
async function sendSlackNotification(slackConfig, message) {
  const fetch = require('node-fetch');
  
  try {
    const slackMessage = {
      text: message.title,
      blocks: [
        {
          type: 'header',
          text: {
            type: 'plain_text',
            text: message.title,
            emoji: true
          }
        },
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `Found *${message.count}* new bounty opportunities!`
          }
        },
        {
          type: 'divider'
        }
      ]
    };

    // Add opportunity details
    message.opportunities.slice(0, 5).forEach(opp => {
      slackMessage.blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*${opp.title}*\n💰 Reward: ${opp.reward || 'N/A'}\n🔗 <${opp.url}|View Opportunity>`
        }
      });
    });

    if (message.count > 5) {
      slackMessage.blocks.push({
        type: 'context',
        elements: [
          {
            type: 'mrkdwn',
            text: `_And ${message.count - 5} more opportunities..._`
          }
        ]
      });
    }

    const response = await fetch(slackConfig.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(slackMessage)
    });

    if (!response.ok) {
      throw new Error(`Slack notification failed with status ${response.status}`);
    }
  } catch (error) {
    console.error('Slack notification failed:', error.message);
    throw error;
  }
}

module.exports = {
  sendBountyAlert,
  sendWebhookNotification,
  sendEmailNotification,
  sendSlackNotification
};
