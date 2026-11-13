const { sendBountyNotification } = require('./services/notificationService');
const { formatBountyNotification } = require('./utils/notificationFormatter');

/**
 * Main entry point for BountyScout
 */
async function main() {
  try {
    // Example usage
    const opportunityCount = 12;
    
    console.log('BountyScout starting...');
    
    // Format and display the notification
    const message = formatBountyNotification(opportunityCount);
    console.log(message);
    
    // Send notifications if channels are configured
    // await sendBountyNotification(opportunityCount, { channels: [] });
    
    console.log('BountyScout completed successfully');
  } catch (error) {
    console.error('Error in BountyScout:', error);
    process.exit(1);
  }
}

// Export for use as a module
module.exports = {
  sendBountyNotification,
  formatBountyNotification
};

// Run if executed directly
if (require.main === module) {
  main();
}
