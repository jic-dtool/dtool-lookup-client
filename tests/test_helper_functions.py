"""Test the 'dtool lookup' command."""


class ResponseMocker(object):

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def test_uris_from_lookup_response():

    from dtool_lookup_client import uris_from_lookup_response

    response = [
          {
            "type": "dataset",
            "uri": "file:///tmp/a_ds",
            "uuid": "af6727bf-29c7-43dd-b42f-a5d7ede28337"
          },
          {
            "type": "dataset",
            "uri": "s3:/dtool-test-s3-bucket/af6727bf-29c7-43dd-b42f-a5d7ede28337",  # NOQA
            "uuid": "af6727bf-29c7-43dd-b42f-a5d7ede28337"
          }
        ]

    uris = uris_from_lookup_response(response)

    expected_content = [
        "file:///tmp/a_ds",
        "s3:/dtool-test-s3-bucket/af6727bf-29c7-43dd-b42f-a5d7ede28337"
    ]
    assert uris == expected_content


def test_urljoin():
    from dtool_lookup_client import urljoin

    assert urljoin(
        "http://localhost:5000",
        "abc",
        "def") == "http://localhost:5000/abc/def"

    assert urljoin(
        "http://localhost:5000/",
        "abc",
        "def") == "http://localhost:5000/abc/def"
