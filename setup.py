import os

from setuptools import setup

setup(
    name="reflex-cli",
    version=f"{os.environ['VERSION']}",
    packages=["reflex_cli", "reflex_cli.commands"],
    include_package_data=True,
    install_requires=[
        "click",
        "jinja2",
        "pyyaml",
        "requests",
        "pyhcl",
        "pyinquirer",
        "pygithub",
    ],
    entry_points="""
        [console_scripts]
        reflex=reflex_cli.cli:cli
    """,
)
