"""Test the dtool_lookup_client package."""


def test_version_is_string():
    import dtool_lookup_client
    assert isinstance(dtool_lookup_client.__version__, str)
