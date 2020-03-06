"""Holder of template generation logic"""
import logging

from reflex_cli.reflex_github import ReflexGithub

LOGGER = logging.getLogger("reflex_cli")


class RuleDiscoverer:
    """Discovers rules by querying github remotes."""

    def __init__(self):
        self.discovered_rules = []

    def collect_rules(self):
        """Collects a list of repos that match rules."""
        repos = ReflexGithub().get_repos()
        self.discovered_rules = self.filter_reflex_repos(repos)
        self.discovered_rules = self.get_repo_versions(self.discovered_rules)
        self.discovered_rules = self.get_rule_modes(self.discovered_rules)

        return self.discovered_rules

    def filter_reflex_repos(self, repos):
        """Determines if a repo name matches the rule naming convention."""
        filtered_repos = []

        for repo in repos:
            LOGGER.debug("Checking repo for %s", repo.name)
            if self.is_rule_repository(repo.name):
                filtered_repos.append(repo)

        return filtered_repos

    @staticmethod
    def get_repo_versions(repos):
        """ Determines the version for each repo and appends it to the repo """
        processed_repos = []

        for repo in repos:
            LOGGER.debug("Getting version for repo %s", repo.name)
            repo.version = ReflexGithub().get_remote_version(
                f"cloudmitigator/{repo.name}"
            )
            processed_repos.append(repo)

        return processed_repos

    @staticmethod
    def get_rule_modes(repos):
        """
        Determines if the rule is able to operate in "remediate" mode

        If so it assigns a "mode" attribute with a value of "remediate"
        """
        processed_repos = []

        for repo in repos:
            LOGGER.debug("Getting mode for repo %s", repo.name)
            mode = ReflexGithub().get_rule_mode(
                f"cloudmitigator/{repo.name}"
            )
            if mode:
                repo.mode = mode
            processed_repos.append(repo)

        return processed_repos

    @staticmethod
    def is_rule_repository(repo_name):
        """Deterministic element for a repository to match a rule."""
        return repo_name.startswith("reflex-aws")

    def display_discovered_rules(self):
        """Method outputs rule information in a usable fashion"""
        LOGGER.info("Rules discovered in CloudMitigator Github organization.")
        LOGGER.info("-------------------------------------------")
        for rule in self.discovered_rules:
            LOGGER.info(
                "\033[4m%s\033[0m: \n\t\033[4mDescription\033[0m:"
                " %s\n\t\033[4mLatest release\033[0m: %s\n",
                rule.name,
                rule.description,
                rule.version,
            )
