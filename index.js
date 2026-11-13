require('dotenv').config();
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatOpportunityMessage } = require('./src/utils/notificationFormatter');

/**
 * Main entry point for BountyScout
 */
async function main() {
  try {
    // Example usage - replace with actual bounty scanning logic
    const opportunityCount = 15;
    
    console.log('BountyScout starting...');
    console.log(formatOpportunityMessage(opportunityCount));
    
    // Send notifications if configured
    const notificationOptions = {
      slack: !!process.env.SLACK_WEBHOOK_URL,
      slackWebhook: process.env.SLACK_WEBHOOK_URL,
      discord: !!process.env.DISCORD_WEBHOOK_URL,
      discordWebhook: process.env.DISCORD_WEBHOOK_URL,
      email: !!process.env.EMAIL_CONFIG,
      emailConfig: process.env.EMAIL_CONFIG
    };
    
    if (notificationOptions.slack || notificationOptions.discord || notificationOptions.email) {
      await sendBountyNotification(opportunityCount, notificationOptions);
      console.log('Notifications sent successfully');
    } else {
      console.log('No notification channels configured');
    }
  } catch (error) {
    console.error('Error in main:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };
