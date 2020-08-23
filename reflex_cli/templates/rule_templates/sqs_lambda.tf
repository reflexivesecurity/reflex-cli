module "sqs_lambda" {
  source           = "git::https://github.com/reflexivesecurity/reflex-engine.git//modules/sqs_lambda?ref={{ engine_version }}"
  cloudwatch_event_rule_id  = var.cloudwatch_event_rule_id
  cloudwatch_event_rule_arn = var.cloudwatch_event_rule_arn
  function_name   = "{{ rule_class_name }}"
  source_code_dir = "${path.module}/../../source"
  handler         = "{{ rule_name.replace('-','_') }}.lambda_handler"
  lambda_runtime  = "python3.7"
  environment_variable_map = {
    SNS_TOPIC = var.sns_topic_arn,
    {% if mode.lower() == "remediate" -%}
    MODE      = var.mode
    {%- endif %}
  }
  custom_lambda_policy = <<EOF
# TODO: Provide required lambda permissions policy
EOF



  queue_name    = "{{ rule_class_name }}"
  delay_seconds = 0

  target_id = "{{ rule_class_name }}"

  sns_topic_arn  = var.sns_topic_arn
  sqs_kms_key_id = var.reflex_kms_key_id
}
