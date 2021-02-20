import asyncio

import click

from app.consumer import main_consumer
from app.producer import main_producer
from app.web_server import run_web_server


@click.command(help='Run producer service')
def run_producer():
    click.echo(click.style('Start producer service', fg='yellow'))

    try:
        asyncio.run(main_producer())
    except KeyboardInterrupt:
        click.echo(click.style('Producer has been stopped', fg='red'))


@click.command(help='Run consumer service')
@click.option('--count', default=3, help='Number of consumers')
def run_consumer(count):
    click.echo(click.style('Start consumer service', fg='yellow'))

    try:
        asyncio.run(main_consumer(count))
    except KeyboardInterrupt:
        click.echo(click.style('Consumer has been stopped', fg='red'))


@click.command(help='Run simple web-server')
def run_web():
    click.echo(click.style('Running web-server...', fg='yellow'))

    run_web_server()


@click.group()
def cli():
    pass


cli.add_command(run_producer)
cli.add_command(run_consumer)
cli.add_command(run_web)


if __name__ == '__main__':
    cli()
