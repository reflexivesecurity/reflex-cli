Reflex Config File: reflex.yaml
----------------------------------
The generated asset of ``reflex init`` is a config file which is by default named ``reflex.yaml``. Below is a reference for the format of that file:

.. code-block:: yaml

  ---
  cli_version: '1.0'


  engine_version: v1.0.0


  globals:
    default_email: administrator@example.com


  backend:
    s3:
    - bucket: example-backend-bucket
    - key: reflex-state


  providers:
  - aws:
      region: us-east-1


  rules:
    aws:
    - enforce-s3-encryption:
        configuration:
        - mode: detect
        version: v0.4.2
    - detect-deactivate-mfa:
        version: v0.3.3
    - detect-root-user-activity:
        version: v0.2.4
    - enforce-no-public-ami:
        configuration:
        - mode: detect
        version: v0.3.2
    - custom-reflex-rule-repository-name:
        configuration:
        - github_org: github_username
        version: v0.0.2
