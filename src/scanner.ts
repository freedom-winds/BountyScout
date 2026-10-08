import { Octokit } from "@octokit/rest";

export interface BountyResult {
  id: number;
  title: string;
  repository: string;
  url: string;
  bounty?: string;
  comments: number;
  updatedAt: string;
}

export class BountyScanner {
  private octokit: Octokit;
  private repos: string[];

  constructor(token: string, repos: string[]) {
    this.octokit = new Octokit({ auth: token });
    this.repos = repos;
  }

  async scan(): Promise<BountyResult[]> {
    const results: BountyResult[] = [];

    for (const repo of this.repos) {
      try {
        const [owner, name] = repo.split("/");
        const issues = await this.octokit.search.issuesAndPullRequests({
          q: `repo:${repo} is:issue label:bounty is:open`,
          per_page: 100,
        });

        for (const issue of issues.data.items) {
          const bountyMatch = issue.title.match(/\$[\d,]+/);
          results.push({
            id: issue.number,
            title: issue.title,
            repository: repo,
            url: issue.html_url,
            bounty: bountyMatch?.[0],
            comments: issue.comments ?? 0,
            updatedAt: issue.updated_at,
          });
        }
      } catch (error) {
        console.error(`Failed to scan ${repo}:`, error);
      }
    }

    return results.sort(
      (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );
  }

  async generateReport(results: BountyResult[]): Promise<string> {
    const scanTime = new Date().toISOString().replace("Z", " UTC");
    let report = `### Active Bounty Scan Results\n\n**Scan Time:** ${scanTime}\n\n`;

    results.forEach((result, index) => {
      report += `#### ${index + 1}. [[Bounty: ${result.bounty || "N/A"}] ${result.title}](${result.url})\n`;
      report += `- **Repository:** [${result.repository}](https://github.com/${result.repository})\n`;
      report += `- **Comments:** ${result.comments}\n`;
      report += `- **Last Updated:** ${result.updatedAt}\n\n`;
    });

    return report;
  }
}
