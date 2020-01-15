from setuptools import setup

setup(
    name="reflex",
    version="0.1.0",
    packages=["reflex_cli", "reflex_cli.commands"],
    include_package_data=True,
    install_requires=["click",],
    entry_points="""
        [console_scripts]
        reflex=reflex_cli.cli:cli
    """,
)
