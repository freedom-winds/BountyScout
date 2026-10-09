const { Octokit } = require('@octokit/rest');
require('dotenv').config();

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

const BOUNTY_KEYWORDS = [
  'bounty', 'bounty proposal', 'bounty:', 'bounty alert',
  'micro bounty', 'BOUNTY-', 'bounty reward'
];

function filterBountyIssues(issues) {
  return issues.filter(issue =>
    BOUNTY_KEYWORDS.some(keyword =>
      issue.title.toLowerCase().includes(keyword.toLowerCase())
    )
  );
}

function generateMarkdownReport({ scanTime, report }) {
  let md = `### Active Bounty Scan Results\n\n`;
  md += `**Scan Time:** ${new Date(scanTime).toISOString().replace('T', ' ').slice(0, 19)} UTC\n\n`;
  
  report.forEach((bounty, index) => {
    md += `#### ${index + 1}. [${bounty.title}](${bounty.url})\n`;
    md += `- **Repository:** ${bounty.repo}\n`;
    md += `- **Comments:** ${bounty.comments}\n`;
    md += `- **Last Updated:** ${new Date(bounty.updated).toISOString().replace('T', ' ').slice(0, 19)}Z\n\n`;
  });

  return md;
}

async function scanRepositories() {
  const repos = [
    'Settla-Labs/settla-api',
    'BasedHardware/omi',
    'Settla-Labs/settla-app',
    'liren001/eth-legion-nexus',
    'duanyytop/agents-radar',
    'dsect-net/quantum',
    'alnitak34/dissent',
    'scapesnovel/AutoCash',
    'scaffold-studio-hq/scaffold-studio-contracts'
  ];

  const report = [];
  const scanTime = new Date().toISOString();

  for (const repo of repos) {
    try {
      const [owner, name] = repo.split('/');
      const { data: issues } = await octokit.rest.issues.listForRepo({
        owner,
        repo: name,
        state: 'open',
        per_page: 100
      });

      const bountyIssues = filterBountyIssues(issues);

      for (const issue of bountyIssues) {
        report.push({
          title: issue.title,
          url: issue.html_url,
          repo: repo,
          comments: issue.comments,
          updated: issue.updated_at
        });
      }
    } catch (error) {
      console.error(`Error scanning ${repo}:`, error.message);
    }
  }

  return { scanTime, report };
}

async function main() {
  const scanResults = await scanRepositories();
  const markdown = generateMarkdownReport(scanResults);
  
  require('fs').writeFileSync('./bounty-report.md', markdown);
  console.log('Bounty scan completed. Report saved to bounty-report.md');
}

module.exports = {
  filterBountyIssues,
  generateMarkdownReport,
  scanRepositories
};

if (require.main === module) {
  main().catch(console.error);
}
