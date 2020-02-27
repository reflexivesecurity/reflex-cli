module "{{module_name}}" {
  source           = "git@github.com:{{github_org}}/{{template_name}}.git?ref={{version}}"
  sns_topic_arn            = module.cental-sns-topic.arn
}
