// Copyright 2026 Freedom Winds. All rights reserved.
import { expect, test, describe, vi } from "vitest";
import { processScanResults } from "../services/bounty-scanner";
import { bulkInsertBounties, updateBountyPriority } from "../database/bounties";
import { notifyMaintainers } from "../services/notifications";

describe("Bounty Scanner", () => {
  test("processScanResults inserts bounties and updates priorities", async () => {
    const mockScanResults = [
      {
        id: "test-1",
        repository: "test/repo",
        issue_url: "https://github.com/test/repo/issues/1",
        title: "Test Bounty",
        comments: 2,
        last_updated: new Date().toISOString(),
      },
    ];

    vi.spyOn(global, "Date").mockImplementation(() => new Date("2026-09-25T05:49:00Z"));
    vi.spyOn(global, "Math").mockImplementation(() => ({
      round: () => 50,
    } as any));

    vi.spyOn(bulkInsertBounties, "mock").mockResolvedValue(undefined);
    vi.spyOn(updateBountyPriority, "mock").mockResolvedValue(undefined);
    vi.spyOn(notifyMaintainers, "mock").mockResolvedValue(undefined);

    await processScanResults(mockScanResults);

    expect(bulkInsertBounties).toHaveBeenCalledWith([
      {
        id: "test-1",
        repository: "test/repo",
        issue_url: "https://github.com/test/repo/issues/1",
        title: "Test Bounty",
        comments: 2,
        last_updated: expect.any(String),
        priority_score: 0,
        base_score: 3,
        maintainer_alert_sent: false,
      },
    ]);

    expect(updateBountyPriority).toHaveBeenCalledWith("test-1");
    expect(notifyMaintainers).toHaveBeenCalledWith([
      {
        id: "test-1",
        repository: "test/repo",
        issue_url: "https://github.com/test/repo/issues/1",
        title: "Test Bounty",
        comments: 2,
        last_updated: expect.any(String),
        priority_score: 0,
        base_score: 3,
        maintainer_alert_sent: false,
      },
    ]);
  });
});