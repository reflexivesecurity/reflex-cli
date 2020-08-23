# reflex-cli

![](https://github.com/reflexivesecurity/reflex-cli/workflows/reflex-cli/badge.svg)

Rapidly generates a configurable infrastructure as code approach to deploying the [reflex infrastructure](https://github.com/reflexivesecurity/reflex-engine). After building the infrastructure code, simply deploy the infrastructure via `terraform`. 

Full reflex documentation (including CLI usage) can be found on our [docs site](https://docs.reflexivesecurity.com).

## Installation

`pip install reflex-cli`

## Basic Usage

1. Generate a configuration file: `reflex init` 
2. Build terraform output files: `reflex build`
3. Deploy those files: `terraform init && terraform apply`
4. Sleep better at night! 

## Demo

![Example CLI usage](/docs/_static/reflex_cli.gif)
