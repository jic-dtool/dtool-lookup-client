"""dtool_lookup_client package."""

import click
import json
import requests

import dtoolcore
import dtoolcore.utils

from dtool_cli.cli import dataset_uri_argument

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


@click.command()
@dataset_uri_argument
@click.option(
    "-s",
    "--server",
    default="http://localhost:5000",
    help="Specify the lookup server")
def register(dataset_uri, server):
    """Return the URIs associated with a UUID in the lookup server."""
    url = urljoin(server, "register_dataset")
    r = requests.get(url)

    dataset = dtoolcore.DataSet.from_uri(dataset_uri)

    dataset_info = dataset._admin_metadata
    dataset_info["uri"] = dataset.uri

    headers = {'content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(dataset_info))
    click.secho(r.text)


@click.command()
@click.argument("query", default="{}")
@click.option(
    "-s",
    "--server",
    default="http://localhost:5000",
    help="Specify the lookup server")
def search(query, server):
    """Return the URIs associated with a UUID in the lookup server."""
    url = urljoin(server, "search_for_datasets")

    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    r = requests.post(url, headers=headers, data=query)
    click.secho(r.text)
