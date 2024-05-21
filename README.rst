README
======

dtool plugin for interacting with dserver

Installation
------------

To install the dtool-lookup-client package.

.. code-block:: bash

    pip install dtool-lookup-client

This plugin depends on having a `dserver
<https://github.com/jic-dtool/dtool-lookup-server>`_ to talk to.

It exposes core functionality of Python API `dtool-lookup-api <https://github.com/livMatS/dtool-lookup-api>`_ on the command line.

Quick start
-----------

Inspect the three core commands with::

    dtool lookup -h
    dtool search -h
    dtool query -h

on the command line.

Configuration
-------------

The plugin needs to know the URL of the lookup server::

    export DSERVER_URL=http://localhost:5000

You also need to specify the access token::

    export DSERVER_TOKEN=$(flask user token olssont)

For testing purposes, it is possible to disable SSL certificates validation with::

    export DSERVER_VERIFY_SSL=false

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

Direct MongoDB No-SQL queries
-----------------------------

This requires a ``dserver`` instance with ``dserver-direct-mongo-plugin``.

To list all datasets created by user ``olssont`` using the mongo query language::

    dtool query '{"creator_username": "olssont"}'
