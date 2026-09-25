// Copyright 2026 Freedom Winds. All rights reserved.
import { expect, test, describe, vi, beforeAll, afterAll } from "vitest";
import { db } from "../db/client";
import { insertBounty, fetchActiveBounties, updateBountyPriority } from "../database/bounties";

describe("Bounty Database", () => {
  beforeAll(async () => {
    await db.delete().from("bounties").execute();
  });

  test("insertBounty adds a bounty to the database", async () => {
    const bounty = {
      id: "test-1",
      repository: "test/repo",
      issue_url: "https://github.com/test/repo/issues/1",
      title: "Test Bounty",
      comments: 2,
      last_updated: new Date().toISOString(),
      priority_score: 0,
      base_score: 10,
      maintainer_alert_sent: false,
    };

    await insertBounty(bounty);
    const result = await db.select().from("bounties").where("id", "test-1").executeTakeFirst();

    expect(result).toEqual(bounty);
  });

  test("fetchActiveBounties retrieves all bounties", async () => {
    const bounty = {
      id: "test-2",
      repository: "test/repo",
      issue_url: "https://github.com/test/repo/issues/2",
      title: "Test Bounty 2",
      comments: 0,
      last_updated: new Date().toISOString(),
      priority_score: 0,
      base_score: 5,
      maintainer_alert_sent: false,
    };

    await insertBounty(bounty);
    const bounties = await fetchActiveBounties();

    expect(bounties).toHaveLength(2);
    expect(bounties).toContainEqual(bounty);
  });

  test("updateBountyPriority updates the priority score", async () => {
    const bounty = {
      id: "test-3",
      repository: "test/repo",
      issue_url: "https://github.com/test/repo/issues/3",
      title: "Test Bounty 3",
      comments: 5,
      last_updated: new Date(Date.now() - 1000 * 60 * 60).toISOString(), // 1 hour ago
      priority_score: 0,
      base_score: 8,
      maintainer_alert_sent: false,
    };

    await insertBounty(bounty);
    await updateBountyPriority("test-3");

    const updatedBounty = await db
      .select()
      .from("bounties")
      .where("id", "test-3")
      .executeTakeFirst();

    expect(updatedBounty.priority_score).toBeGreaterThan(0);
    expect(updatedBounty.last_updated).toBeDefined();
  });
});