import { Agent } from '@langchain/langgraph';
import type { Config } from './types/index.js';
import { AlertService } from './services/alert.service.js';
import { formatBountyAlertTitle } from './utils/formatters.js';

class BountyScout {
  private agent: Agent;
  private alertService: AlertService;
  private config: Config;

  constructor(config: Config) {
    this.config = config;
    this.agent = this.initializeAgent();
    this.alertService = new AlertService(config);
  }

  private initializeAgent(): Agent {
    // Initialize the scanning agent
    return new Agent({
      model: this.config.agent_model,
      tools: ['github_search', 'gitlab_search'],
    });
  }

  async scanAndAlert(): Promise<void> {
    const opportunities = await this.agent.scan();
    await this.alertService.createBountyAlert(opportunities);
  }

  async start(): Promise<void> {
    console.log('🚀 Starting BountyScout...');
    await this.scanAndAlert();
  }
}

// CLI entry point
const config: Config = {
  github_token: process.env.GITHUB_TOKEN ?? '',
  database_url: process.env.DATABASE_URL ?? '',
  agent_model: process.env.AGENT_MODEL ?? 'gpt-4o-mini',
  crawl_delay: parseInt(process.env.CRAWL_DELAY ?? '30', 10),
  openai_api_key: process.env.OPENAI_API_KEY ?? '',
  github_worker_enabled: process.env.GITHUB_WORKER_ENABLED !== 'false',
};

const scout = new BountyScout(config);
scout.start().catch(console.error);
