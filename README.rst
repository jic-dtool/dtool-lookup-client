README
======

Dtool plugin for interacting with dtool lookup server

Installation
------------

To install the dtool_lookup_client package.

.. code-block:: bash

    pip install dtool_lookup_client

This plugin depends on having a `dtool-lookup-server
<https://github.com/jic-dtool/dtool-lookup-server>`_ to talk to.

Configuration
-------------

The plugin needs to know the URL of the lookup server::

    export DTOOL_LOOKUP_SERVER_URL=http://localhost:5000

You also need to specify the access token::

    export DTOOL_LOOKUP_SERVER_TOKEN=$(flask user token olssont)

For testing purposes, it is possible to disable SSL certificates validation with::

    export DTOOL_LOOKUP_CLIENT_IGNORE_SSL=true

Looking up datasets by UUID
---------------------------

To lookup URIs from a dataset UUID::

    dtool lookup UUID

Searching
---------

To list all registered datasets::

    dtool search

Full text search for the word "EMS"::

    dtool search EMS

To list all datasets created by user ``olssont`` using the mongo query language::

    dtool search -m '{"creator_username": "olssont"}'
