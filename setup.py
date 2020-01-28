from setuptools import setup

setup(
    name="reflex-cli",
    version="0.0.1",
    packages=["reflex_cli", "reflex_cli.commands"],
    package_data={"reflex_cli": ["templates/*"]},
    include_package_data=True,
    install_requires=["click", "jinja2", "pyyaml"],
    entry_points="""
        [console_scripts]
        reflex=reflex_cli.cli:cli
    """,
)
