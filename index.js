require('dotenv').config();
const { sendBountyNotification } = require('./src/services/notificationService');
const { formatBountyNotification } = require('./src/utils/notificationFormatter');

/**
 * Main entry point for BountyScout
 */
async function main() {
  try {
    console.log('BountyScout started...');
    
    // Example usage - replace with actual bounty discovery logic
    const mockOpportunities = [
      { title: 'Example Bounty 1', url: 'https://example.com/1', description: 'Test bounty' },
      { title: 'Example Bounty 2', url: 'https://example.com/2', description: 'Another test' }
    ];
    
    if (mockOpportunities.length > 0) {
      await sendBountyNotification(mockOpportunities.length, mockOpportunities);
    }
    
  } catch (error) {
    console.error('Error in main:', error);
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
