module "cwe" {
  source           = "git::https://github.com/reflexivesecurity/reflex-engine.git//modules/cwe?ref={{ engine_version }}"
  name        = "{{ rule_class_name }}"
  description = "TODO: Provide rule description"

  event_pattern = <<PATTERN
# TODO: Provide event pattern
PATTERN
}
