module "{{module_name}}" {
  source            = "git::https://github.com/{{github_org}}/{{template_name}}.git?ref={{version}}"
  sns_topic_arn     = module.central-sns-topic.arn
  reflex_kms_key_id = module.reflex-kms-key.key_id
{%- if configuration -%}
  {%- for configurable in configuration -%}
    {%- if configurable is mapping %}
      {%- for key, value in configurable.items() %}
        {%- if value is mapping %}
    {{key}}              = {
      {%- for map_key, map_value in value.items() %}
      {{map_key}}: {{map_value}}
      {%- endfor %}
    }
        {%- else %}
    {{key}}              = "{{value}}"
        {%- endif %}
    {%- endfor %}
    {%- else %}
    {{configurable}}   = ""
    {%- endif %}
  {%- endfor %}
{%- endif %}
}
