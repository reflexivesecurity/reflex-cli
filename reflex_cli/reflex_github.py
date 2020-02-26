"""Holder of template generation logic"""
import logging
import os

import github

LOGGER = logging.getLogger("reflex_cli")


class ReflexGithub:
    """Discovers measures by querying github remotes."""

    def __init__(self):
        self.github_organizations = ["cloudmitigator"]

        token = os.environ.get("REFLEX_GITHUB_TOKEN")
        self.github_client = github.Github(token)

    def get_repos(self):
        """Iterates over github org and collects repos that match rules."""
        for organization in self.github_organizations:  # pragma: no cover
            LOGGER.debug("Collecting repos for %s", organization)
            org_api = self.github_client.get_organization(organization)
            return org_api.get_repos()

    def get_remote_version(self, remote):
        """Calls github API for remote to get latest release."""
        try:  # pragma: no cover
            repo = self.github_client.get_repo(remote)
        except github.GithubException:  # pragma: no cover
            LOGGER.debug("No remote resource found at github.com/%s", remote)
            return None
        try:  # pragma: no cover
            latest_release = repo.get_latest_release()
        except github.GithubException:  # pragma: no cover
            LOGGER.debug("No releases found for %s", remote)
            return None
        return latest_release.tag_name
