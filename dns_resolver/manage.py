import click
import socket
from resolver import DNSResolver


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host_ip', default=None, help='IP for server')
@click.option('--port', default=53, type=int, help='Port for server to listen on')
@click.option('--bind_path', default='bind.example.txt', help='Path to bind file')
def run(host_ip, port, bind_path):
    click.echo("Starting UDP server...")

    if not host_ip:
        localhost = socket.gethostname()
        host_ip = socket.gethostbyname(localhost)

    resolver = DNSResolver(bind_path=bind_path)
    resolver.listen(host_ip=host_ip, port=int(port))


if __name__ == "__main__":
    cli()
