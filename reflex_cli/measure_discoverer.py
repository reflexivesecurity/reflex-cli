"""Holder of template generation logic"""
import logging

from reflex_cli.reflex_github import ReflexGithub

LOGGER = logging.getLogger("reflex_cli")


class MeasureDiscoverer:
    """Discovers measures by querying github remotes."""

    def __init__(self):
        self.discovered_measures = []

    def collect_measures(self):
        """Collects a list of repos that match rules."""
        repos = ReflexGithub().get_repos()
        self.discovered_measures = self.filter_reflex_repos(repos)
        return self.discovered_measures

    def filter_reflex_repos(self, repos):
        """Determines if a repo name matches the rule naming convention."""
        filtered_repos = []

        for repo in repos:
            LOGGER.debug("Checking repo for %s", repo.name)
            if self.is_rule_repository(repo.name):
                repo.version = ReflexGithub().get_remote_version(
                    f"cloudmitigator/{repo.name}"
                )
                filtered_repos.append(repo)
        return filtered_repos

    @staticmethod
    def is_rule_repository(repo_name):
        """Deterministic element for a repository to match a rule."""
        return repo_name.startswith("reflex-aws")

    def display_discovered_measures(self):
        """Method outputs measure information in a usable fashion"""
        LOGGER.info("Rules discovered in CloudMitigator Github organization.")
        LOGGER.info("-------------------------------------------")
        for measure in self.discovered_measures:
            LOGGER.info(
                "\033[4m%s\033[0m: \n\t\033[4mDescription\033[0m:"
                " %s\n\t\033[4mLatest release\033[0m: %s\n",
                measure.name,
                measure.description,
                measure.version,
            )
