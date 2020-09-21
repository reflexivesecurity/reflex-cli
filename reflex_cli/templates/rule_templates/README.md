# {{ rule_name }}

TODO: Write a brief description of your rule and what it does.

## Usage

To use this rule either add it to your `reflex.yaml` configuration file:

```
rules:
  - {{ rule_name }}:
      version: latest
{%- if mode.lower() == "remediate" %}
      configuration:
        mode: remediate
{%- endif %}
```

or add it directly to your Terraform:

```
...

module "{{ rule_name }}-cwe" {
  source            = "git::https://github.com/{{ github_org_name }}/{{ rule_name }}.git//terraform/cwe?ref=latest"
}

module "{{ rule_name }}" {
  source            = "git::https://github.com/{{ github_org_name }}/{{ rule_name }}.git?ref=latest"
  sns_topic_arn     = module.central-sns-topic.arn
  reflex_kms_key_id = module.reflex-kms-key.key_id
{%- if mode.lower() == "remediate" %}
  mode              = "remediate"
{%- endif %}
}

...
```

Note: The `sns_topic_arn` and `reflex_kms_key_id` example values shown here assume you generated resources with `reflex build`. If you are using the Terraform on its own you need to provide your own valid values.

{%- if mode.lower() == "remediate" %}

## Configuration
This rule has the following configuration options:

<dl>
  <dt>mode</dt>
  <dd>
  <p>Sets the rule to operate in <code>detect</code> or <code>remediate</code> mode.</p>

  <em>Required</em>: No  

  <em>Type</em>: string

  <em>Possible values</em>: `detect` | `remediate`  

  <em>Default</em>: `detect`
  </dd>
</dl>
{%- endif %}

## Contributing
If you are interested in contributing, please review [our contribution guide](https://docs.reflexivesecurity.com/about/contributing.html).

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view
the [LICENSE](https://github.com/{{ github_org_name
}}/{{ rule_name }}/blob/master/LICENSE)
