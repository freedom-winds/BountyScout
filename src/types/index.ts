export interface Repository {
  id: string;
  full_name: string;
  description: string | null;
  language: string | null;
  url: string;
  last_scanned_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Issue {
  id: string;
  repository_id: string;
  number: number;
  title: string;
  body: string | null;
  url: string;
  state: 'open' | 'closed';
  labels: string[];
  bounty_amount?: number | null;
  bounty_currency?: string | null;
  bounty_source?: string | null;
  created_at: string;
  updated_at: string;
}

export interface BountyOpportunity {
  id: string;
  issue_id: string;
  repository_id: string;
  confidence_score: number;
  category: string;
  estimated_complexity: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface BountyAlert {
  id: string;
  scan_time: string;
  total_opportunities: number;
  new_opportunities: number;
  opportunities: BountyOpportunityDetail[];
  created_at: string;
}

export interface BountyOpportunityDetail extends BountyOpportunity {
  issue: Issue;
  repository: Repository;
}

export interface ScanResult {
  repository: Repository;
  new_issues: Issue[];
  updated_issues: Issue[];
  identified_bounties: BountyOpportunity[];
  scan_duration_ms: number;
}

export interface Config {
  github_token: string;
  database_url: string;
  agent_model: string;
  crawl_delay: number;
  openai_api_key: string;
  slack_webhook?: string;
  redis_url?: string;
  github_worker_enabled: boolean;
}
