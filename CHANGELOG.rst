CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Changed
^^^^^^^

- Build system switched to hatchling with hatch-vcs; the version is now
  derived from git tags
- Require ``dtool-cli>=0.7.2``; earlier releases import ``pkg_resources``,
  which is not available without setuptools


Removed
^^^^^^^

- Support for Python < 3.10


[0.2.0]
-------

Added
^^^^^

- ``dtool lookup`` command
- ``dtool search`` command
- ``dtool query`` command
- ``dtool config lookup_server url`` command
- ``dtool config lookup_server token`` command


Changed
^^^^^^^

- rebranded some bits from ``dtool_lookup_...`` to ``dserver_...``

Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


