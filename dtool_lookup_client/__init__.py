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
import dtool_config.cli

CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH

DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"


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
    url = urljoin(server, "dataset", "lookup", uuid)
    token = dtoolcore.utils.get_config_value("DTOOL_LOOKUP_SERVER_TOKEN")
    headers = {
        "Authorization": "Bearer {}".format(token),
    }
    r = requests.get(url, headers=headers)
    for uri in uris_from_lookup_response(r):
        click.secho(uri)


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


@dtool_config.cli.config.group()
def lookup_server():
    """Configure dtool lookup server connection."""


@lookup_server.command()
@click.argument("dtool_lookup_server_url", required=False)
def url(dtool_lookup_server_url):
    """Display / set / update the dtool lookup server URL."""
    if dtool_lookup_server_url is None:
        click.secho(dtoolcore.utils.get_config_value_from_file(
            DTOOL_LOOKUP_SERVER_URL_KEY, default=""
        ))
    else:
        click.secho(dtoolcore.utils.write_config_value_to_file(
            DTOOL_LOOKUP_SERVER_URL_KEY,
            dtool_lookup_server_url
        ))
