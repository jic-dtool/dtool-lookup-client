README
======

Dtool plugin for interacting with dtool lookup server

To install the dtool_lookup_client package.

.. code-block:: bash

    cd dtool_lookup_client
    python setup.py install

Full text search for the word "EMS"::

    dtool search '{"$text": {"$search": "EMS"}}'
