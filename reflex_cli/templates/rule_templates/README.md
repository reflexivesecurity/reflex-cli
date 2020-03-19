# {{ rule_name }}
TODO: Write a brief description of your rule and what it does.

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:  
```
rules:
  - {{ rule_name }}:
      version: latest
```

or add it directly to your Terraform:  
```
...

module "{{ rule_name }}" {
  source           = "github.com/{{ github_org_name }}/{{ rule_name }}"
}

...
```

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/{{ github_org_name }}/{{ rule_name }}/blob/master/LICENSE) 
