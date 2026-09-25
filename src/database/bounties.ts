// Copyright 2026 Freedom Winds. All rights reserved.
import { Bounty } from "../types/bounty";
import { db } from "../db/client";

const bountyTable = "bounties";

/**
 * Inserts a new bounty opportunity into the database.
 * @param bounty - Bounty object with metadata.
 */
export const insertBounty = async (bounty: Bounty): Promise<void> => {
  await db.insert(bountyTable).values(bounty).execute();
};

/**
 * Fetches all active bounties with optional filtering.
 * @param filters - Optional filters (e.g., repository, priority).
 */
export const fetchActiveBounties = async (filters?: Partial<Bounty>): Promise<Bounty[]> => {
  return db
    .select()
    .from(bountyTable)
    .where(filters)
    .execute();
};

/**
 * Updates the priority score of a bounty based on recent activity.
 * @param bountyId - ID of the bounty to update.
 */
export const updateBountyPriority = async (bountyId: string): Promise<void> => {
  const bounty = await db
    .select()
    .from(bountyTable)
    .where("id", bountyId)
    .executeTakeFirstOrThrow();

  const newScore = calculatePriorityScore(bounty);
  await db
    .update(bountyTable)
    .set({
      priority_score: newScore,
      last_updated: new Date().toISOString(),
    })
    .where("id", bountyId)
    .execute();
};

/**
 * Calculates priority score based on repository activity, comments, and age.
 */
const calculatePriorityScore = (bounty: Bounty): number => {
  const hoursSinceUpdate = (new Date().getTime() - new Date(bounty.last_updated).getTime()) / (1000 * 60 * 60);
  const commentWeight = bounty.comments * 0.3;
  const ageWeight = Math.max(0, 24 - hoursSinceUpdate) * 0.2;
  return Math.round(commentWeight + ageWeight + bounty.base_score);
};

/**
 * Bulk inserts new bounties from a scan.
 * @param bounties - Array of bounty objects.
 */
export const bulkInsertBounties = async (bounties: Bounty[]): Promise<void> => {
  await db.insert(bountyTable).values(bounties).execute();
}