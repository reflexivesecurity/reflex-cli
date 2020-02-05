"""Holder of template generation logic"""
import logging
import os

import github

LOGGER = logging.getLogger("reflex_cli")


class MeasureDiscoverer:
    """Discovers measures by querying github remotes."""

    def __init__(self):
        self.discovered_measures = {}
        self.github_organizations = ["cloudmitigator"]

        if os.environ.get("REFLEX_GITHUB_TOKEN"):
            self.github_client = github.Github(
                os.environ.get("REFLEX_GITHUB_TOKEN")
            )
        else:
            self.github_client = github.Github()

    def collect_measures(self):
        """Iterates over github org and collects repos that match rules."""
        for organization in self.github_organizations:
            LOGGER.debug("Collecting repos for %s", organization)
            org_api = self.github_client.get_organization(organization)
            rule_repositories = self.filter_reflex_repos(org_api)
            self.discovered_measures[organization] = rule_repositories

    def filter_reflex_repos(self, org_api):
        """Determines if a repo name matches the rule convention naming."""
        filtered_repos = []
        for repo in org_api.get_repos():
            LOGGER.debug("Checking repo for %s", repo.name)
            if self.is_rule_repository(repo.name):
                filtered_repos.append(repo)
        return filtered_repos

    @staticmethod
    def is_rule_repository(repo_name):
        """Deterministic element for a repository to match a rule."""
        return repo_name.startswith("reflex-aws")

    def display_discovered_measures(self):
        """Method outputs measure information in a usable fashion"""
        for organization in self.github_organizations:
            LOGGER.info(
                "Rules discovered in %s Github organization.", organization
            )
            LOGGER.info("-------------------------------------------")
            for rule_repo in self.discovered_measures[organization]:
                LOGGER.info("%s: %s", rule_repo.name, rule_repo.description)
