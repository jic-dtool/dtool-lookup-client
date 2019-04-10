"""dtool_lookup_client package."""

import click
import json
import requests

from datetime import date, datetime

import yaml

import pygments
import pygments.lexers
import pygments.formatters

import dtoolcore
import dtoolcore.utils


__version__ = "0.1.0"

# This needs to be below __version__ to prevent issues with import ordering.
# Ideally the code below should be in separate modules.
from dtool_cli.cli import dataset_uri_argument


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} not serializable".format(type(obj)))


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

    # Add the readme info.
    readme_info = yaml.load(dataset.get_readme_content())
    dataset_info["readme"] = readme_info

    headers = {'content-type': 'application/json'}
    data = json.dumps(dataset_info, default=json_serial)
    r = requests.post(url, headers=headers, data=data)
    click.secho(r.text)


@click.command()
@click.argument("query", default="")
@click.option("-m", "--mongosyntax", default=False, is_flag=True)
@click.option(
    "-s",
    "--server",
    default="http://localhost:5000",
    help="Specify the lookup server")
def search(query, mongosyntax, server):
    """Return the URIs associated with a UUID in the lookup server."""
    url = urljoin(server, "dataset", "search")

    if not mongosyntax:
        if query == "":
            query = "{}"
        else:
            query = '{"$text": {"$search": "' + query + '"}}'

    token = dtoolcore.utils.get_config_value("DTOOL_LOOKUP_SERVER_TOKEN")
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    r = requests.get(url)
    r = requests.post(url, headers=headers, data=query)

    formatted_json = json.dumps(json.loads(r.text), indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())

    click.secho(colorful_json, nl=False)
