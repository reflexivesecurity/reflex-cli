module "central-sns-topic" {
  topic_name         = "ReflexAlerts"
  stack_name         = "EmailSNSStackReflexAlerts"
  source             = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/sns_email_subscription?ref={{engine_version}}"
  notification_email = "{{ email }}"
}
