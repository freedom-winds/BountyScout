const { formatOpportunityMessage } = require('./utils/notificationFormatter');
const { sendBountyNotification } = require('./services/notificationService');

/**
 * Main function to scan for bounties and send notifications
 */
async function scanBounties() {
  try {
    // Scan for new bounty opportunities
    const opportunities = await fetchNewOpportunities();
    const count = opportunities.length;
    
    // Send notification with proper grammar
    if (count > 0) {
      await sendBountyNotification(count, {
        slack: {
          webhookUrl: process.env.SLACK_WEBHOOK_URL,
          username: 'BountyScout',
          icon: ':dart:',
        },
        discord: {
          webhookUrl: process.env.DISCORD_WEBHOOK_URL,
          username: 'BountyScout',
        },
      });
    }
    
    return opportunities;
  } catch (error) {
    console.error('Error scanning bounties:', error);
    throw error;
  }
}

/**
 * Fetches new bounty opportunities
 * @returns {Promise<Array>} Array of opportunities
 */
async function fetchNewOpportunities() {
  // Implementation would fetch from various bounty platforms
  // This is a placeholder that should be replaced with actual logic
  return [];
}

module.exports = {
  scanBounties,
  formatOpportunityMessage,
  sendBountyNotification,
};
