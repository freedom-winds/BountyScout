// src/utils/bounty_utils.test.ts
import { BountyScanner } from '../models/bounty'
import { describe, expect, test } from '@jest/globals'

describe('BountyScanner', () => {
  test('parses scan result into bounties', () => {
    const rawScan = `1. [[Bounty proposal] fix(backend): sanitize errors ($50)](https://example.com/repo)
2. [Security audit needed]($1000) - https://example.com/audit`
    const bounties = BountyScanner.parseScanResult(rawScan)
    expect(bounties.length).toBe(2)
    expect(bounties[0].title).toBe('fix(backend): sanitize errors')
    expect(bounties[0].rewardAmount).toBe(50)
    expect(bounties[1].rewardAmount).toBe(1000)
  })

  test('handles malformed URLs', () => {
    const rawScan = `1. [Invalid URL](not-a-url)`
    const bounties = BountyScanner.parseScanResult(rawScan)
    expect(bounties[0].repository).toBe('')
  })

  test('calculates priority score correctly', () => {
    const titleWithComments = 'Bounty with 3 comments'
    const bounty = new BountyScanner()
    expect(bounty.calculatePriorityScore(titleWithComments)).toBe(1)
    expect(bounty.calculatePriorityScore(titleWithComments, 100)).toBe(3)
  })
})