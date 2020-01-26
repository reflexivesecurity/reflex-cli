provider "aws" {
  region = "us-east-1"
}

module "enforce_s3_encryption" {
  source           = "git@github.com:cloudmitigator/reflex-aws-enforce-s3-encryption"
  email            = "{{ email }}"
}
