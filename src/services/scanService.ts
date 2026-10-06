import { Octokit } from "@octokit/rest";
import type { Config } from "../config/types.js";
import type { BountyAlert } from "../types/index.js";

const octokit = new Octokit();

export async function performBountyScan(config: Config): Promise<BountyAlert[]> {
  const results: BountyAlert[] = [];
  const repositories = config.bountyRepositories || [];

  for (const repo of repositories) {
    try {
      const issues = await octokit.issues.listForRepo({
        owner: repo.split("/")[0],
        repo: repo.split("/")[1],
        state: "open",
        per_page: 100,
      });

      for (const issue of issues.data) {
        if (isBountyIssue(issue)) {
          results.push({
            id: issue.id,
            title: issue.title,
            url: issue.html_url,
            repository: repo,
            comments: issue.comments,
            lastUpdated: issue.updated_at,
            createdAt: issue.created_at,
          });
        }
      }
    } catch (error) {
      console.error(`Failed to scan ${repo}:`, error);
    }
  }

  return results.sort(
    (a, b) =>
      new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime(),
  );
}

function isBountyIssue(issue: {
  title: string;
  body?: string;
  labels?: { name: string }[];
}): boolean {
  const labels = issue.labels?.map((l) => l.name.toLowerCase()) || [];
  const titleLower = issue.title.toLowerCase();
  const bodyLower = (issue.body || "").toLowerCase();

  const bountyKeywords = ["bounty", "opportunity", "help wanted", "micro bounty"];
  const hasKeyword = bountyKeywords.some(
    (kw) => titleLower.includes(kw) || bodyLower.includes(kw),
  );
  const hasBountyLabel = labels.some(
    (l) => l.includes("bounty") || l.includes("opportunity"),
  );

  return hasKeyword || hasBountyLabel;
}
