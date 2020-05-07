module "{{cwe_module_name}}" {
  source            = "git::https://github.com/{{github_org}}/{{template_name}}.git//terraform/cwe?ref={{version}}"
}

module "{{module_name}}" {
  source            = "git::https://github.com/{{github_org}}/{{template_name}}.git//terraform/sqs_lambda?ref={{version}}"
  cloudwatch_event_rule_id = module.{{cwe_module_name}}.id
  cloudwatch_event_rule_arn = module.{{cwe_module_name}}.arn
  sns_topic_arn     = module.central-sns-topic.arn
  reflex_kms_key_id = module.reflex-kms-key.key_id

{%- if configuration -%}
  {%- for key, value in configuration.items() -%}
    {%- if value is mapping %}

  {{key}} = {
      {%- for map_key, map_value in value.items() %}
    {{map_key}}: {{map_value}}
      {%- endfor %}
  }

    {%- elif value is iterable %}
      {{key}} = "{{value | safe}}"

    {%- else %}

  {{key}} = "{{value}}"

    {%- endif %}
  {%- endfor %}
{%- endif %}
}
