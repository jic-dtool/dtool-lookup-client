"""dtool_lookup_client package."""

import click
import requests

__version__ = "0.1.0"


def uris_from_lookup_response(response):
    """Return list of URIs from  response from /lookup_datasets/<uuid>."""
    return [item["uri"] for item in response.json()]


def urljoin(*args):
    parts = []
    for p in args:
        if p.endswith("/"):
            p = p[:-1]
        parts.append(p)
    return "/".join(parts)


@click.command()
@click.argument("uuid")
@click.option(
    "-s",
    "--server",
    default="http://localhost:5000",
    help="Specify the lookup server")
def lookup(uuid, server):
    """Return the URIs associated with a UUID in the lookup server."""
    url = urljoin(server, "lookup_datasets", uuid)
    r = requests.get(url)
    for uri in uris_from_lookup_response(r):
        click.secho(uri)
