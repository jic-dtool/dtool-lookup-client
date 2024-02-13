"""Test the dserver_client package."""


def test_version_is_string():
    import dserver_client
    assert isinstance(dserver_client.__version__, str)
