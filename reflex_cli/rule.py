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

    @property
    def github_org(self):
        """Returns the GitHub organization that owns this Rule.

        Returns:
            str: GitHub organization name
        """
        if "github_org" in self.raw_rule:
            return self.raw_rule["github_org"]
        return "cloudmitigator"

    @property
    def repository_name(self):
        """Returns the repository name for this Rule.

        Returns:
            str: The repository name
        """
        if "github_org" in self.raw_rule:
            return self.name
        return f"reflex-aws-{self.name}"

    @property
    def remote_url(self):
        """Returns the remote repository URL.

        Returns:
            str: The remote repository URL
        """
        return f"https://github.com/{self.github_org}/{self.repository_name}"
