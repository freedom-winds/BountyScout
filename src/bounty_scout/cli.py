import click
from .services.bounty_integration import BountyIntegrationService
from .storage.database import BountyDatabase


@click.group()
@click.pass_context
def cli(ctx):
    """Bounty Scout CLI for managing bounty opportunities."""
    ctx.ensure_object(dict)
    ctx.obj['db'] = BountyDatabase()


@cli.command()
@click.pass_context
def scan():
    """Scans for new bounty opportunities and integrates them."""
    db = context.obj['db']
    service = BountyIntegrationService(db)
    result = service.process_latest_scan()
    click.echo(f"Scanned {len(result.opportunities)} new opportunities at {result.scan_time.isoformat()}")


@cli.command()
@click.option('--limit', default=20, help='Number of recent opportunities to display')
@click.pass_context
def list(limit):
    """Lists the most recent bounty opportunities."""
    db = context.obj['db']
    service = BountyIntegrationService(db)
    opportunities = service.get_recent_opportunities(limit)
    for opportunity in opportunities:
        tags = ', '.join(opportunity.bounty_tags) if opportunity.bounty_tags else 'None'
        click.echo(f"[{opportunity.scan_timestamp.isoformat()}] {opportunity.repository} | {opportunity.title} | Tags: {tags}")