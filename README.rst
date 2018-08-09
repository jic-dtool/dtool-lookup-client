README
======

Dtool plugin for interacting with dtool lookup server

Installation
------------

To install the dtool_lookup_client package.

.. code-block:: bash

    cd dtool_lookup_client
    python setup.py install

This plugin depends on having a `dtool-lookup-server
<https://github.com/jic-dtool/dtool-lookup-server>`_ to talk to.

Registering datasets
--------------------

To register a dataset::

    dtool register DATASET_URI

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
