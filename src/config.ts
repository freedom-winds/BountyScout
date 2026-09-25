// src/config.ts
import dotenv from 'dotenv'

dotenv.config()

export const config = {
  slackWebhook: process.env.SLACK_WEBHOOK_URL || 'https://hooks.slack.com/services/...',
  discordWebhook: process.env.DISCORD_WEBHOOK_URL || 'https://discord.com/api/webhooks/...',
  bountyScoutDomain: process.env.BOUNTY_SCOUT_DOMAIN || 'https://bountyscout.app',
  maxBountyAgeDays: parseInt(process.env.MAX_BOUNTY_AGE_DAYS || '30'),
  priorityThresholds: {
    low: 2,
    medium: 5,
    high: 10
  }
}