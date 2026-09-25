// Copyright 2026 Freedom Winds. All rights reserved.
import { Bounty, ScanResult } from "../types/bounty";
import { bulkInsertBounties, updateBountyPriority } from "../database/bounties";
import { notifyMaintainers } from "../services/notifications";

/**
 * Processes scan results and updates the bounty database.
 * @param scanResults - Array of scan results from GitHub.
 */
export const processScanResults = async (scanResults: ScanResult[]): Promise<void> => {
  const bounties: Bounty[] = scanResults.map((result) => ({
    id: result.id,
    repository: result.repository,
    issue_url: result.issue_url,
    title: result.title,
    comments: result.comments,
    last_updated: result.last_updated,
    priority_score: 0,
    base_score: calculateBaseScore(result),
    maintainer_alert_sent: false,
  }));

  await bulkInsertBounties(bounties);
  await updatePriorities(bounties);
  await notifyMaintainers(bounties);
};

/**
 * Calculates base score for a bounty based on repository activity.
 */
const calculateBaseScore = (result: ScanResult): number => {
  const repoActivity = getRepositoryActivity(result.repository);
  return Math.round(repoActivity * 10);
};

/**
 * Mock: Fetches repository activity score (placeholder for real implementation).
 */
const getRepositoryActivity = (repository: string): number => {
  // In production, this would fetch from GitHub API or cache.
  const activityMap: Record<string, number> = {
    "woahwhattheheck/commons": 0.8,
    "MentorsMind/MentorsMind-Contract": 0.7,
    "CitrateNetwork/citrate-cluster": 0.9,
    "degenspot/BACKit-onStellar": 0.6,
    "decred/dcrlnd": 0.5,
  };
  return activityMap[repository] || 0.3;
};

/**
 * Updates priority scores for all newly inserted bounties.
 */
const updatePriorities = async (bounties: Bounty[]): Promise<void> => {
  for (const bounty of bounties) {
    await updateBountyPriority(bounty.id);
  }
}