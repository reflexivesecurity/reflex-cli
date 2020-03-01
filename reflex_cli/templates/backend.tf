terraform {
  backend "{{backend_type}}" {
{% for backend_config in backend_config_array -%}
{%- for key, value in backend_config.items() %}
    {{key}} = "{{value}}"
{%- endfor %}
{%- endfor %}
  }
}
