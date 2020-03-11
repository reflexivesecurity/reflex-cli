module "{{module_name}}" {
  source            = "git::https://github.com/{{github_org}}/{{template_name}}.git?ref={{version}}"
  sns_topic_arn     = module.central-sns-topic.arn
  reflex_kms_key_id = module.reflex-kms-key.key_id
{%- if configuration -%}
{%- for configurable in configuration -%}
  {%- for key in configurable %}
  {{key}}              = "{{configurable[key]}}"
{%- endfor %}
{%- endfor %}
{%- endif %}
}
