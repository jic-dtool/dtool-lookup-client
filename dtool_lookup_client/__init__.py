"""dtool_lookup_client package."""

from datetime import date, datetime

import click
import json

import pygments
import pygments.lexers
import pygments.formatters

import dtoolcore
import dtoolcore.utils
import dtool_config.cli
import dtool_lookup_api

__version__ = "0.1.0"

DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} not serializable".format(type(obj)))


def uris_from_lookup_response(response):
    """Return list of URIs from  response from /lookup_datasets/<uuid>."""
    return [item["uri"] for item in response]


def urljoin(*args):
    parts = []
    for p in args:
        if p.endswith("/"):
            p = p[:-1]
        parts.append(p)
    return "/".join(parts)


@click.command()
@click.argument("uuid")
def lookup(uuid):
    """Print the URIs associated with a UUID in the lookup server."""
    r = dtool_lookup_api.lookup(uuid)
    for uri in uris_from_lookup_response(r):
        click.secho(uri)


@click.command()
@click.argument("keyword", default="")
def search(keyword):
    """Print metadata matching keyword(s) on the lookup server."""
    r = dtool_lookup_api.search(keyword)
    formatted_json = json.dumps(r, indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())

    click.secho(colorful_json, nl=False)


@click.command()
@click.argument("query", default="")
def query(query):
    """Print metadata associated with a query in the lookup server."""
    r = dtool_lookup_api.query(query)
    formatted_json = json.dumps(r, indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())

    click.secho(colorful_json, nl=False)


#############################################################################
# Add click group to 'dtool config' with options for configuring connection
# to the dtool lookup server.
#############################################################################

@dtool_config.cli.config.group()
def lookup_server():
    """Configure dtool lookup server connection."""


@lookup_server.command()
@click.argument("dtool_lookup_server_url", required=False)
def url(dtool_lookup_server_url):
    """Display / set / update URL for dtool lookup server."""
    if dtool_lookup_server_url is None:
        click.secho(dtoolcore.utils.get_config_value_from_file(
            DTOOL_LOOKUP_SERVER_URL_KEY, default=""
        ))
    else:
        click.secho(dtoolcore.utils.write_config_value_to_file(
            DTOOL_LOOKUP_SERVER_URL_KEY,
            dtool_lookup_server_url
        ))


@lookup_server.command()
@click.argument("dtool_lookup_server_token", required=False)
def token(dtool_lookup_server_token):
    """Display / set / update token for dtool lookup server."""
    if dtool_lookup_server_token is None:
        click.secho(dtoolcore.utils.get_config_value_from_file(
            DTOOL_LOOKUP_SERVER_TOKEN_KEY, default=""
        ))
    else:
        click.secho(dtoolcore.utils.write_config_value_to_file(
            DTOOL_LOOKUP_SERVER_TOKEN_KEY,
            dtool_lookup_server_token
        ))
