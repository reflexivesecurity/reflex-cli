variable "sns_topic_arn" {
  description = "SNS topic arn of central or local sns topic"
  type        = string
}

variable "reflex_kms_key_id" {
  description = "KMS Key Id for common reflex usage."
  type        = string
}

variable "cloudwatch_event_rule_id" {
  description = "Easy name of CWE"
  type        = string
}

variable "cloudwatch_event_rule_arn" {
  description = "Full arn of CWE"
  type        = string
}

{% if mode.lower() == "remediate" -%}
variable "mode" {
  description = "The mode that the Rule will operate in. Valid choices: DETECT | REMEDIATE"
  type        = string
  default     = "detect"
}
{%- endif %}
