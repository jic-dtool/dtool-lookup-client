from setuptools import setup

url = "https://github.com/jic-dtool/dtool-lookup-client"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool_lookup_client",
    packages=["dtool_lookup_client"],
    version=version,
    description="Dtool plugin for interacting with dtool lookup server",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
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
