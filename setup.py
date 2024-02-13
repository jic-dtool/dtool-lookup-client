import os
from setuptools import setup

url = "https://github.com/livMatS/dserver-client"
readme = open('README.rst').read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="dserver_client",
    packages=["dserver_client"],
    description="Dtool plugin for interacting with dserver",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    use_scm_version={
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join("dserver_client", "version.py"),
        "local_scheme": local_scheme},
    setup_requires=[
        'setuptools_scm'
    ],
    url=url,
    install_requires=[
        "asgiref",
        "click",
        "requests",
        "dtoolcore>=3.9.0",
        "dtool-cli>=0.7.1",
        "dtool_config>=0.1.1",
        "dtool-lookup-api>=0.5.0",
        "pygments",
    ],
    entry_points={
        "dtool.cli": [
            "lookup=dserver_client:lookup",
            "search=dserver_client:search",
            "query=dserver_client:query",
        ],
    },
    license="MIT"
)
