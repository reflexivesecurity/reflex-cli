module "detect_deactivate_mfa" {
  source           = "git@github.com:cloudmitigator/reflex-aws-detect-deactivate-mfa"
  email            = "{{ email }}"
}

