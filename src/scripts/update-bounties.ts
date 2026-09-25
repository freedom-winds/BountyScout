#!/usr/bin/env node
// Copyright 2026 Freedom Winds. All rights reserved.
import { fetchActiveBounties as fetchFromGitHub } from "../utils/github";
import { processScanResults } from "../services/bounty-scanner";

/**
 * Script to update bounties from GitHub scan results.
 */
(async () => {
  try {
    console.log("Fetching active bounties from GitHub...");
    const scanResults = await fetchFromGitHub();
    console.log(`Found ${scanResults.length} active bounties.`);

    console.log("Processing scan results...");
    await processScanResults(scanResults);
    console.log("Bounties updated successfully.");
  } catch (error) {
    console.error("Failed to update bounties:", error);
    process.exit(1);
  }
})();