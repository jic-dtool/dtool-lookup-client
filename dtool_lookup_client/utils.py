"""dtool_lookup_client.utils module."""

import dtoolcore.utils

from asgiref.sync import async_to_sync

# TODO: standardize LookupClient API
from dtool_lookup_gui.LookupClient import LookupClient

from .config import (
    DTOOL_LOOKUP_SERVER_URL_KEY,
    DTOOL_LOOKUP_SERVER_TOKEN_KEY,
    DTOOL_LOOKUP_SERVER_USERNAME_KEY,
    DTOOL_LOOKUP_SERVER_PASSWORD_KEY)


async def connect():
    """Connect to dtool lookup server session."""
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


def _get_authorisation_header_value():
    token = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_TOKEN_KEY)
    if token is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_TOKEN_KEY))
    return "Bearer {}".format(token)


@async_to_sync
async def async_lookup(uuid):
    """Wraps around asynchronous LookupClient method 'by_uuid'."""
    lookup_client = await connect()
    try:
        r = await lookup_client.by_uuid(uuid)
    finally:
        await lookup_client.session.close()
    return r


@async_to_sync
async def async_search(keyword):
    """Wraps around asynchronous LookupClient method 'search'."""
    lookup_client = await connect()
    try:
        r = await lookup_client.search(keyword)
    finally:
        await lookup_client.session.close()
    return r


@async_to_sync
async def async_query(query):
    """Wraps around asynchronous LookupClient method 'query'."""
    lookup_client = await connect()
    try:
        r = await lookup_client.by_query(query)
    finally:
        await lookup_client.session.close()  # TODO: shouldn't that happen transparently somewhere else?
    return r


def lookup(uuid):
    """Return the URIs associated with a UUID in the lookup server."""
    r = async_lookup(uuid)
    return r


def search(keyword):
    """Return the URIs associated with a UUID in the lookup server."""
    r = async_search(keyword)
    return r


def query(query, mongosyntax):
    """Return the URIs associated with a query in the lookup server."""
    if not mongosyntax:
        if query == "":
            query = "{}"
        else:
            query = '{"$text": {"$search": "' + query + '"}}'

    r = async_query(query)
    return r
