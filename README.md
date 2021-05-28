# Supported tags and respective Dockerfile links

- [`1.0.0`, `latest`](https://github.com/ets-infra/drone-github-full-release/blob/master/1/Dockerfile)

# Quick reference (cont.)

- **Where to file issues**: [https://github.com/ets-infra/drone-github-full-release/issues](https://github.com/ets-infra/drone-github-full-release/issues)

# What is the purpose of this image?

[Drone](https://www.drone.io) plugin to switch a GitHub pre-release to a full-release.

<p align="center">
    <a href="https://www.drone.io"><img alt="drone logo" src="https://raw.githubusercontent.com/drone/brand/master/logos/png/dark/drone-logo-png-dark-128.png"></a>
</p>

The following steps are executed by this plugin:

1. Gather the latest version number based on changelog.
2. Update the GitHub release for this version to a full release.

| Parameter | Description |
|:---|---|
| changelog_path | Path to the changelog. Default to `CHANGELOG.md` in current folder. |
| github_token | Token (repo permission) used to update the release. Default to [the drone GIT password](https://docs.drone.io/server/reference/drone-git-password/) (if available). Related user needs to have admin role in repository. |

# How to use this image

## Add a step to your drone pipeline

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: tag
  image: etsinfra/drone-github-full-release:latest
  settings:
    changelog_path: custom_folder/CHANGELOG.md
    github_token: cc1cc11111111ccc1c11c1cc1ccc1c1cc1111c1c
```
