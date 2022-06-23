import os
from setuptools import setup

url = "https://github.com/IMTEK-Simulation/dtool-lookup-api"
readme = open('README.rst').read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="dtool_lookup_client",
    packages=["dtool_lookup_client"],
    description="Dtool plugin for interacting with dtool lookup server",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    use_scm_version={
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join("dtool_lookup_api", "version.py"),
        "local_scheme": local_scheme},
    setup_requires=[
        'setuptools_scm>=3.5.0'
    ],
    url=url,
    install_requires=[
        "asgiref",
        "click",
        "requests",
        "dtoolcore>=3.9.0",
        "dtool_config>=0.1.1",
        "dtool-lookup-api>=0.1",
        "pygments",
    ],
    entry_points={
        "dtool.cli": [
            "lookup=dtool_lookup_client:lookup",
            "search=dtool_lookup_client:search",
            "query=dtool_lookup_client:query",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
