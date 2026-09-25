// Copyright 2026 Freedom Winds. All rights reserved.
import { Octokit } from "@octokit/rest";
import { ScanResult } from "../types/bounty";

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
});

/**
 * Fetches active bounty opportunities from GitHub.
 * @returns Array of scan results.
 */
export const fetchActiveBounties = async (): Promise<ScanResult[]> => {
  const issues = await octokit.request("GET /search/issues", {
    q: "is:issue is:open label:bounty",
    per_page: 100,
  });

  return issues.data.items.map((item) => ({
    id: item.number.toString(),
    repository: item.repository.full_name,
    issue_url: item.html_url,
    title: item.title,
    comments: item.comments,
    last_updated: item.updated_at,
  }));
};

/**
 * Fetches repository metadata (e.g., maintainer info).
 */
export const fetchRepositoryMetadata = async (repository: string): Promise<any> => {
  return octokit.request(`GET /repos/${repository}`, {});
}