"""dtool_lookup_client package."""

__version__ = "0.1.0"


def uris_from_lookup_response(response):
    """Return list of URIs from  response from /lookup_datasets/<uuid>."""
    return [item["uri"] for item in response.json()]
