// Copyright 2026 Freedom Winds. All rights reserved.

/**
 * Represents a bounty opportunity with metadata.
 */
export interface Bounty {
  id: string;
  repository: string;
  issue_url: string;
  title: string;
  comments: number;
  last_updated: string;
  priority_score: number;
  base_score: number;
  maintainer_alert_sent: boolean;
  tags?: string[];
}

/**
 * Represents a bounty scan result from GitHub.
 */
export interface ScanResult {
  id: string;
  repository: string;
  issue_url: string;
  title: string;
  comments: number;
  last_updated: string;
}