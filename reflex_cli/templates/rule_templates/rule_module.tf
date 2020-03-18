module "{{ rule_name.replace('-','_') }}" {
  source           = "git::https://github.com/cloudmitigator/reflex-engine.git//modules/cwe_lambda?ref={{ engine_version }}"
  rule_name        = "{{ rule_class_name }}"
  rule_description = "TODO: Provide rule description"

  event_pattern = <<PATTERN
# TODO: Provide event pattern
PATTERN

  function_name   = "{{ rule_class_name }}"
  source_code_dir = "${path.module}/source"
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
