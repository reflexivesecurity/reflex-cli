
from cloudmitigator_semantic.git import GitActions
from setuptools import setup
current_version = GitActions().version.version

setup(
    name="reflex-cli",
    version=current_version,
    packages=["reflex_cli", "reflex_cli.commands"],
    package_data={"reflex_cli": ["templates/*"]},
    include_package_data=True,
    install_requires=["click", "jinja2", "pyyaml", "pygithub"],
    entry_points="""
        [console_scripts]
        reflex=reflex_cli.cli:cli
    """,
)
