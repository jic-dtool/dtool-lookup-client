README
======

tool plugin for interacting with dserver

Installation
------------

To install the dserver_client package.

.. code-block:: bash

    pip install dserver_client

This plugin depends on having a `dserver
<https://github.com/jic-dtool/dserver>`_ to talk to.

Configuration
-------------

The plugin needs to know the URL of the lookup server::

    export DSERVER_URL=http://localhost:5000

You also need to specify the access token::

    export DSERVER_TOKEN=$(flask user token olssont)

For testing purposes, it is possible to disable SSL certificates validation with::

    export DSERVER_CLIENT_IGNORE_SSL=true

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
