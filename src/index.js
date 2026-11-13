const NotificationService = require('./services/notificationService');
const { formatBountyNotification } = require('./utils/notificationFormatter');

// Initialize notification service
const notificationService = new NotificationService();

// Example: Register console logger as default handler
notificationService.registerHandler((notification) => {
  console.log(`[${notification.timestamp}] ${notification.message}`);
  if (notification.opportunities) {
    console.log('Opportunities:', notification.opportunities);
  }
});

/**
 * Main function to process and notify about new bounties
 * @param {Array} opportunities - Array of new opportunities found
 * @returns {Promise<void>}
 */
async function processBounties(opportunities = []) {
  try {
    if (!Array.isArray(opportunities)) {
      throw new Error('Opportunities must be an array');
    }

    const count = opportunities.length;
    
    await notificationService.sendBountyAlert(count, {
      opportunities: opportunities.map(opp => ({
        title: opp.title || 'Untitled',
        url: opp.url || '',
        platform: opp.platform || 'unknown',
        reward: opp.reward || 'N/A'
      }))
    });

    return {
      success: true,
      count,
      message: formatBountyNotification(count)
    };
  } catch (error) {
    console.error('Error processing bounties:', error);
    throw error;
  }
}

module.exports = {
  notificationService,
  processBounties,
  formatBountyNotification
};
