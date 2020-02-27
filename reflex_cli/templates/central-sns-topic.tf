module "central-sns-topic" {
  topic_name         = "ReflexAlerts"
  stack_name         = "EmailSNSStackReflexAlerts"
  source             = "git@github.com:cloudmitigator/reflex-engine.git//modules/sns_email_subscription"
  notification_email = "{{ email }}"
}
