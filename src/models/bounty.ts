// src/models/bounty.ts
import { Timestamp } from "@typegoose/typegoose/lib/types"

export interface Bounty {
  id: string
  repository: string
  title: string
  description: string
  priorityScore: number
  rewardAmount: number | null
  lastUpdated: Timestamp
  sourceScanId: string
  status: 'open' | 'claimed' | 'expired'
  claimedAt?: Timestamp
  metadata: Record<string, unknown>
}

export class BountyScanner {
  static parseScanResult(raw: string): Bounty[] {
    const bountyRegex = /(\[\[].*?\]\()?([^)]+)(\s*\$\d+)?/g
    const matches = raw.matchAll(bountyRegex)
    return Array.from(matches).map((match) => {
      const [full, title, rewardText] = match
      const rewardAmount = rewardText ? parseInt(rewardText.replace(/\$|,/g, '')) : null
      return {
        id: crypto.randomUUID(),
        repository: this.extractRepositoryUrl(title),
        title: this.sanitizeTitle(title),
        description: this.truncateDescription(title),
        priorityScore: this.calculatePriorityScore(title, rewardAmount),
        rewardAmount,
        lastUpdated: new Date(),
        sourceScanId: crypto.randomUUID(),
        status: 'open',
        metadata: {}
      }
    })
  }

  private static extractRepositoryUrl(title: string): string {
    const urlMatch = title.match(/https:\/\/github\.com\/[^\s]+/)
    return urlMatch ? urlMatch[0] : ''
  }

  private static sanitizeTitle(title: string): string {
    return title.replace(/(\[\[]|\]\()|(\$\d+)/g, '').trim()
  }

  private static truncateDescription(title: string): string {
    return title.length > 100 ? title.substring(0, 97) + '...' : title
  }

  private static calculatePriorityScore(title: string, reward?: number): number {
    const commentCount = this.countComments(title)
    const rewardFactor = reward ? Math.log10(reward) : 0
    return Math.floor(commentCount * 0.5 + rewardFactor * 2)
  }

  private static countComments(title: string): number {
    const commentMatch = title.match(/Comments:\s*(\d+)/)
    return commentMatch ? parseInt(commentMatch[1]) : 0
  }
}