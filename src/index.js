require('dotenv').config();
const { sendBountyNotification } = require('./services/notificationService');

/**
 * Main application entry point
 */
async function main() {
  try {
    console.log('BountyScout started...');
    
    // Example usage - replace with actual bounty scanning logic
    const mockOpportunities = [
      {
        title: 'XSS Vulnerability in Login Form',
        url: 'https://example.com/bounty/1',
        description: 'Cross-site scripting vulnerability found in login form',
        reward: '$500-$1000',
        platform: 'HackerOne'
      },
      {
        title: 'SQL Injection in Search',
        url: 'https://example.com/bounty/2',
        description: 'SQL injection vulnerability in search functionality',
        reward: '$1000-$2500',
        platform: 'Bugcrowd'
      }
    ];
    
    // Send notification for found opportunities
    await sendBountyNotification(mockOpportunities.length, mockOpportunities);
    
  } catch (error) {
    console.error('Error in main application:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };
