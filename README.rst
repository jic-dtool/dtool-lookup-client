README
======

Dtool plugin for interacting with dtool lookup server

Installation
------------

To install the dtool_lookup_client package.

.. code-block:: bash

    cd dtool_lookup_client
    python setup.py install

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

To list all datasets created by user ``olssont``::

    dtool search '{"creator_username": "olssont"}'

