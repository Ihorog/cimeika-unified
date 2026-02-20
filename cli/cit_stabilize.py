#!/usr/bin/env python3
import click
import requests
import os
import sys


@click.command()
@click.option('--draft', type=click.File('r'), required=True, help='Draft file to stabilize')
@click.option('--intent', default='', help='User intent/context')
@click.option('--mode', type=click.Choice(['normal', 'smart', 'critical']), default='normal')
@click.option('--output', type=click.File('w'), default='-', help='Output file (default: stdout)')
@click.option('--api-url', envvar='CI_API_URL', default='http://localhost:8000', help='API base URL')
@click.option('--api-key', envvar='CI_ADMIN_KEY', required=True, help='Admin API key')
def stabilize(draft, intent, mode, output, api_url, api_key):
    """Stabilize AI draft text using ci_axis.yaml rules"""
    draft_text = draft.read()

    response = requests.post(
        f"{api_url}/stabilizer/stabilize",
        json={
            "draft": draft_text,
            "intent": intent,
            "mode": mode
        },
        headers={"X-CI-Key": api_key}
    )

    if response.status_code != 200:
        click.echo(f"Error: {response.status_code} - {response.text}", err=True)
        sys.exit(1)

    result = response.json()
    output.write(result["final"])

    # Print report to stderr
    report = result["report"]
    click.echo(f"\n--- Stabilization Report ---", err=True)
    click.echo(f"Trace ID: {report['trace_id']}", err=True)
    click.echo(f"Cut flags: {', '.join(report['cut_flags']) or 'none'}", err=True)
    click.echo(f"Trimmed chars: {report['trimmed_chars']}", err=True)
    click.echo(f"Removed topics: {report['removed_new_topics']}", err=True)
    click.echo(f"Deterministic score: {report['deterministic_score']:.3f}", err=True)


if __name__ == '__main__':
    stabilize()
