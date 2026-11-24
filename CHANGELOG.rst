CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^

- ``dtool query`` command


Changed
^^^^^^^

- Build system switched to hatchling with hatch-vcs; the version is now
  derived from git tags
- Require ``dtool-cli>=0.7.2``; earlier releases import ``pkg_resources``,
  which is not available without setuptools
- The publish workflow now runs only for version tags: it runs the test
  suite, checks that the built version matches the tag and publishes to
  PyPI. Development builds are no longer uploaded to TestPyPI
- Rebranded some bits from ``dtool_lookup_...`` to ``dserver_...``


Deprecated
^^^^^^^^^^


Removed
^^^^^^^

- Support for Python < 3.10


Fixed
^^^^^


Security
^^^^^^^^


[0.1.0] - 2019-04-10
--------------------

Added
^^^^^

- ``dtool lookup`` command
- ``dtool search`` command
- ``dtool config lookup_server url`` command
- ``dtool config lookup_server token`` command
