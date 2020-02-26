module "{{module_name}}" {
  source           = "git@github.com:{{github_org}}/{{template_name}}.git?ref={{version}}"
  email            = "{{ email }}"
}
