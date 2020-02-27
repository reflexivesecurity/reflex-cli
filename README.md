# reflex CLI

The reflex cli (command Line interface) tool enables guardrail developers to leverage
the reflex framework.

## Requirements

1. Python 3.7.x
2. Terraform v0.12.x

## Setup

```sh
pip install reflex-cli
```

## Usage

### Show help

```sh
reflex --help
```

### Initialize reflex

```sh
reflex init
```

Launches a wizard to generate a `reflex.yaml` configuration file for use during a build
of reflex.

### Build reflex

```sh
reflex build
```

Take a local `reflex.yaml` and generate terraform templates based on the measures
specified.

### Show rules

```sh
reflex show
```

Display discovered measures via the CLI.

### Deploy reflex

```sh
reflex tf [terraform_args]
```

From output directory of the build, use `reflex tf` to map to `terraform` commands
(`apply`, `plan`).

## Development

Install deveopment dependencies in `requirements.txt`.

```sh
pip install -r requirements.txt
```

Install in editable mode.

Note: This will also install dependencies specified in `setup.py`

```sh
pip install -e .
```
