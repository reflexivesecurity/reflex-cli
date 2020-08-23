module "{{module_name}}" {
  source            = "git::https://github.com/{{github_org}}/{{template_name}}.git//terraform/cwe?ref={{version}}"
}

module "forwarder-{{module_name}}" {
  source            = "git::https://github.com/reflexivesecurity/reflex-engine.git//modules/sns_cross_region_sqs?ref={{engine_version}}"
  kms_key_id = module.reflex-kms-key.key_id
  cloudwatch_event_rule_id = module.{{module_name}}.id
  central_region = "{{central_region}}"
  central_queue_name = "{{queue_name}}"
}
