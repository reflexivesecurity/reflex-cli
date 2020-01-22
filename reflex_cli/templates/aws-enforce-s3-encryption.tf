provider "aws" {
  region = "us-east-1"
}

module "enforce_s3_encryption" {
  source           = "github.com/cloudmitigator/reflex-aws-enforce-s3-encryption?ref=0.0.1"
  email            = "{{ email }}"
}

