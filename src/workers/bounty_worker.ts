// src/workers/bounty_worker.ts
import { BountyScanner } from '../models/bounty'
import { BountyAlertGenerator } from '../services/alert_generator'
import { BountyService } from '../services/bounty.service'
import { config } from '../config'

export class BountyWorker {
  private bountyService: BountyService
  private slackWebhook: string
  private discordWebhook: string

  constructor() {
    this.bountyService = new BountyService()
    this.slackWebhook = config.slackWebhook
    this.discordWebhook = config.discordWebhook
  }

  async processScanResult(rawScan: string): Promise<void> {
    const bounties = BountyScanner.parseScanResult(rawScan)
    for (const bounty of bounties) {
      await this.bountyService.createOrUpdate(bounty)
      this.sendAlerts(bounty)
    }
  }

  private sendAlerts(bounty: any): void {
    const slackMessage = BountyAlertGenerator.generateSlackEmbed(bounty)
    const discordMessage = BountyAlertGenerator.generateDiscordMessage(bounty)

    // Simulate sending alerts (actual HTTP calls would go here)
    console.log('Slack Alert:', slackMessage)
    console.log('Discord Alert:', discordMessage)
  }
}