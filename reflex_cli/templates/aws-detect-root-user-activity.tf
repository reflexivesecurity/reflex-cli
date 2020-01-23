module "detect_root_user_activity" {
  source           = "git@github.com:cloudmitigator/reflex-aws-detect-root-user-activity"
  email            = "{{ email }}"
}
