import datetime
import os

import keepachangelog
import requests


class GitHub:
    def __init__(self):
        token = os.getenv('PLUGIN_GITHUB_TOKEN', os.getenv("DRONE_GIT_PASSWORD"))
        if not token:
            raise Exception("github_token parameter must be provided as DRONE_GIT_PASSWORD environment variable is not set.")

        github_link = os.getenv("DRONE_REPO_LINK")[:-len(os.getenv("DRONE_REPO"))]
        self.base_url = f"{github_link}api/v3/repos/{os.getenv('DRONE_REPO')}"
        self.client = requests.Session()
        self.client.headers = {'Authorization': f"token {token}", "Accept": "application/vnd.github.v3+json"}

    def get(self, uri: str) -> requests.Response:
        response = self.client.get(
            url=f"{self.base_url}{uri}",
        )
        response.raise_for_status()
        return response

    def patch(self, uri: str, content: dict) -> requests.Response:
        response = self.client.patch(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to PATCH to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

    def release(self, tag: str, new_title: str, extra_content: str):
        previous = self.get(f"/releases/tags/{tag}").json()
        self.patch(
            f"/releases/{previous['id']}",
            {
                "name": new_title,
                "body": f"{extra_content}\n{previous['body']}",
                "prerelease": False
            }
        )


def create_github_release():
    release = get_latest_version(os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md"))

    technical_information = f"Release done on {datetime.date.today().isoformat()} ({datetime.datetime.utcnow().isoformat()} UTC)"

    print(f"Switching GitHub pre-release to full release ({release['metadata']['version']} tag).")

    GitHub().release(
        tag=release["metadata"]["version"],
        new_title=f"{release['metadata']['version']} ({datetime.date.today().isoformat()})",
        extra_content=technical_information,
    )


def get_latest_version(changelog_path: str) -> dict:
    releases = keepachangelog.to_raw_dict(changelog_path)
    new_version, _ = keepachangelog.to_sorted_semantic(releases.keys())[-1]
    return releases[new_version]


if __name__ == "__main__":
    create_github_release()
