// src/services/alert_generator.ts
import { Bounty } from '../models/bounty'
import { SlackMessage, DiscordMessage } from '../types/alert_types'

export class BountyAlertGenerator {
  static generateSlackEmbed(bounty: Bounty): SlackMessage {
    const priorityColor = bounty.priorityScore > 5 ? '#FF0000' : 
                          bounty.priorityScore > 2 ? '#FFD700' : '#00FF00'
    return {
      text: `🚨 New Bounty Alert: ${bounty.title}`,
      attachments: [{
        color: priorityColor,
        title: bounty.title,
        title_link: bounty.repository,
        text: bounty.description,
        fields: [
          { title: 'Reward', value: bounty.rewardAmount ? `$${bounty.rewardAmount.toLocaleString()}` : 'Unspecified', short: true },
          { title: 'Priority', value: bounty.priorityScore.toString(), short: true },
          { title: 'Last Updated', value: bounty.lastUpdated.toISOString(), short: true }
        ],
        footer: 'BountyScout | Source: GitHub'
      }]
    }
  }

  static generateDiscordMessage(bounty: Bounty): DiscordMessage {
    return {
      content: `**New Bounty Opportunity**
**Title:** ${bounty.title}
**Repository:** ${bounty.repository}
**Description:** ${bounty.description}
**Reward:** ${bounty.rewardAmount ? `$${bounty.rewardAmount}` : 'Unspecified'}
**Priority:** ${bounty.priorityScore}
[View on GitHub](${bounty.repository})`,
      embeds: []
    }
  }

  static generateEmailDigest(bounties: Bounty[]): string {
    return `BountyScout Daily Digest (${new Date().toISOString().split('T')[0]})

${bounties.map(b => `• [${b.title}](${b.repository}) - $${b.rewardAmount || '?'} (Priority: ${b.priorityScore})`).join('\n')}

View all: https://bountyscout.app/bounties`
  }
}