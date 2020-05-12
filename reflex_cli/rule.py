"""Properties for our Rule object in the CLI."""

DEFAULT_VARIABLES = [
    "sns_topic_arn",
    "reflex_kms_key_id",
    "cloudwatch_event_rule_id",
    "cloudwatch_event_rule_arn",
]


class Rule:
    """Base class that represents a rule object to the CLI."""

    def __init__(self, rule_name, rule_dict):
        self.name = rule_name
        self.raw_rule = rule_dict
        self.version = rule_dict.get("version")
        self.description = rule_dict.get("description")
        self.variables = rule_dict.get("variables")

    @property
    def configurables(self):
        """Displays configurable elements of a Rule."""
        configurables = []
        for variable in self.variables:
            if variable not in DEFAULT_VARIABLES:
                configurables.append(variable)
        return configurables

    @property
    def numeric_version(self):
        """Returns a version dictionary for major minor patch."""
        raw_version = self.version.replace("v", "")
        split_version = raw_version.split(".")
        return {
            "major": split_version[0],
            "minor": split_version[1],
            "patch": split_version[2],
        }
