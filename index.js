require('dotenv').config();
const { sendBountyNotification } = require('./src/services/notificationService');

/**
 * Main entry point for BountyScout
 */
async function main() {
  try {
    console.log('BountyScout started...');
    
    // Example usage - replace with actual bounty scanning logic
    const mockOpportunities = [
      {
        title: 'Web Application Security Testing',
        url: 'https://example.com/bounty/1',
        description: 'Find vulnerabilities in our web application',
        reward: '$500-$5000',
        platform: 'HackerOne'
      },
      {
        title: 'Mobile App Bug Bounty',
        url: 'https://example.com/bounty/2',
        description: 'Security testing for mobile applications',
        reward: '$1000-$10000',
        platform: 'Bugcrowd'
      }
    ];
    
    // Send notification for found opportunities
    await sendBountyNotification(12, mockOpportunities);
    
    console.log('BountyScout completed successfully');
  } catch (error) {
    console.error('Error in BountyScout:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { main };
