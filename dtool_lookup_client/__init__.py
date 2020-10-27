"""dtool_lookup_client package."""

from asgiref.sync import async_to_sync
import click
import json
import requests

from datetime import date, datetime

import pygments
import pygments.lexers
import pygments.formatters

import dtoolcore
import dtoolcore.utils
import dtool_config.cli

from dtool_lookup_gui.LookupClient import LookupClient

CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH

DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"
DTOOL_LOOKUP_SERVER_USERNAME_KEY = "DTOOL_LOOKUP_SERVER_USERNAME"
DTOOL_LOOKUP_SERVER_PASSWORD_KEY = "DTOOL_LOOKUP_SERVER_PASSWORD"

DTOOL_LOOKUP_CLIENT_IGNORE_SSL_KEY = "DTOOL_LOOKUP_CLIENT_IGNORE_SSL"

__version__ = "0.1.0"


async def connect():
    lookup_url = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_URL_KEY)
    if lookup_url is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_URL_KEY))

    auth_url = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_TOKEN_KEY)
    if auth_url is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_TOKEN_KEY))

    username = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_USERNAME_KEY)
    if username is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_USERNAME_KEY))

    password = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_PASSWORD_KEY)
    if username is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_PASSWORD_KEY))

    lookup_client = LookupClient(lookup_url, auth_url, username, password)

    await lookup_client.connect()

    return lookup_client
    # self.server_config = await self.lookup.config()
    #    self.datasets = await self.lookup.all()


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


def _get_authorisation_header_value():
    token = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_TOKEN_KEY)
    if token is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_TOKEN_KEY))
    return "Bearer {}".format(token)


@async_to_sync
async def async_lookup(uuid):
    lookup_client = await connect()
    r = await lookup_client.by_uuid(uuid)
    await lookup_client.session.close()  # TODO: shouldn't that happen transparently elsewhere?
    return r


@click.command()
@click.argument("uuid")
def lookup(uuid):
    """Return the URIs associated with a UUID in the lookup server."""
    r = async_lookup(uuid)
    for uri in uris_from_lookup_response(r):
        click.secho(uri)


@click.command()
@click.argument("query", default="")
@click.option("-m", "--mongosyntax", default=False, is_flag=True)
def search(query, mongosyntax):
    """Return the URIs associated with a UUID in the lookup server."""
    server = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_URL_KEY)
    verify = not dtoolcore.utils.get_config_value(
        DTOOL_LOOKUP_CLIENT_IGNORE_SSL_KEY, default=False)
    url = urljoin(server, "dataset", "search")

    if not mongosyntax:
        if query == "":
            query = "{}"
        else:
            query = '{"$text": {"$search": "' + query + '"}}'

    headers = {
        "Authorization": _get_authorisation_header_value(),
        "Content-Type": "application/json"
    }
    r = requests.get(url, verify=verify)
    r = requests.post(url, headers=headers, data=query, verify=verify)

    formatted_json = json.dumps(json.loads(r.text), indent=2)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())

    click.secho(colorful_json, nl=False)


@async_to_sync
async def async_query(query):
    lookup_client = await connect()
    r = await lookup_client.by_query(query)
    await lookup_client.session.close()  # TODO: shouldn't that happen transparently somewhere else?
    return r


@click.command()
@click.argument("query", default="")
@click.option("-m", "--mongosyntax", default=False, is_flag=True)
def query(query, mongosyntax):
    """Return the URIs associated with a query in the lookup server."""
    if not mongosyntax:
        if query == "":
            query = "{}"
        else:
            query = '{"$text": {"$search": "' + query + '"}}'

    r = async_query(query)
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
