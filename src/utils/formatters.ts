import type { BountyOpportunityDetail } from '../types/index.js';

const OPPORTUNITY_TEXT = 'Opportunity';

export function formatOpportunityText(count: number): string {
  const word = count === 1 ? OPPORTUNITY_TEXT : `${OPPORTUNITY_TEXT}s`;
  return word;
}

export function formatBountyAlert(opportunities: BountyOpportunityDetail[]): string {
  const opportunityWord = opportunities.length === 1 ? OPPORTUNITY_TEXT : `${OPPORTUNITY_TEXT}s`;

  const items = opportunities.map((opp, index) => {
    const repo = opp.repository;
    const issue = opp.issue;
    const bountyInfo =
      opp.bounty_amount
        ? ` — $${opp.bounty_amount} ${opp.bounty_currency ?? 'USD'}`
        : '';

    return `#### ${index + 1}. [${issue.title}](https://github.com/${repo.full_name}/issues/${issue.number})${bountyInfo}`;
  });

  return `### Active Bounty Scan Results\n\n**Scan Time:** ${new Date().toISOString().replace('Z', 'Z')}\n\n${items.join('\n\n')}`;
}

export function formatBountyAlertTitle(count: number): string {
  const opportunityWord = count === 1 ? OPPORTUNITY_TEXT : `${OPPORTUNITY_TEXT}s`;
  return `🎯 Bounty Alert: ${count} New ${opportunityWord} found`;
}
