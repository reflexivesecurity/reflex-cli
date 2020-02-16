module "{{module_name}}" {
  source           = "git@github.com:cloudmitigator/{{template_name}}.git?ref={{version}}"
  email            = "{{ email }}"
}
