---
prev_status: success
next_action: write
status: success
---
# BountyScout

[![Discord](https://img.shields.io/discord/1330274858470765669?logo=discord)](https://discord.gg/bountyscout)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fbounty.scout)](https://bounty.scout)

## Overview

BountyScout is an AI-driven system that monitors GitHub and GitLab repositories for new bounty opportunities. It helps developers find paid issues across various projects, making it easier to discover and contribute to open-source work with financial incentives.

## 🚀 Quick Start

### Local Development (Recommended)

Clone the repository and run the following commands:

```bash
# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env

# Run the application
pnpm dev
```

### Docker

Build and run using Docker Compose:

```bash
docker compose up --build
```

## ⚙️ Configuration

To set up the app, copy `.env.example` to `.env` and configure the required variables:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost:5432/bountyscout` |
| `GITHUB_TOKEN` | GitHub personal access token | `ghp_xxxxxxxx` |
| `AGENT_MODEL` | Model identifier for the agent | `gpt-4o-mini` |
| `CRAWL_DELAY` | Delay between repository crawls (in seconds) | `30` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GITHUB_WORKER_ENABLED` | Enable GitHub worker | `true` |
| `SLACK_WEBHOOK` | Slack webhook URL for notifications | - |
| `REDIS_URL` | Redis connection URL | - |

## 🏗️ Architecture

BountyScout uses a distributed worker architecture:

- **Scheduler**: Periodically triggers repository scans
- **Worker**: Processes individual repositories
- **Processor**: Analyzes issues and identifies bounty opportunities
- **Notifier**: Sends alerts via Discord

## 📖 Documentation

For detailed documentation, visit [docs.bounty.scout](https://docs.bounty.scout).

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Discord](https://discord.gg/bountyscout)
- [Website](https://bounty.scout)
- [Documentation](https://docs.bounty.scout)
