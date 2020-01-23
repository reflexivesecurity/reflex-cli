module "enforce_no_public_ami" {
  source           = "git@github.com:cloudmitigator/reflex-aws-enforce-no-public-ami"
  email            = "{{ email }}"
}

