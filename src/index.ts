import { BountyScanner } from "./scanner";

const REPOS = process.env.BOUNTY_REPOS?.split(",") || [];
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || "";

async function main() {
  if (!GITHUB_TOKEN) {
    console.error("GITHUB_TOKEN environment variable is required");
    process.exit(1);
  }

  const scanner = new BountyScanner(GITHUB_TOKEN, REPOS);
  const results = await scanner.scan();

  if (results.length > 0) {
    const report = await scanner.generateReport(results);
    console.log(report);
  } else {
    console.log("No new bounties found.");
  }
}

main().catch(console.error);
