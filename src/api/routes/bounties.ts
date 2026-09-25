// Copyright 2026 Freedom Winds. All rights reserved.
import { Router } from "express";
import { fetchActiveBounties as fetchFromDB } from "../../database/bounties";
import { Bounty } from "../../types/bounty";

const router = Router();

/**
 * GET /api/bounties/active
 * Fetches all active bounties with optional filters.
 */
router.get("/active", async (req, res) => {
  try {
    const filters = req.query;
    const bounties = await fetchFromDB(filters as Partial<Bounty>);
    res.json(bounties);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch bounties" });
  }
});

/**
 * GET /api/bounties/active/recent
 * Fetches recently updated bounties (last 24 hours).
 */
router.get("/active/recent", async (req, res) => {
  try {
    const twentyFourHoursAgo = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const bounties = await fetchFromDB({
      last_updated: { ">": twentyFourHoursAgo },
    });
    res.json(bounties);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch recent bounties" });
  }
});

export default router;