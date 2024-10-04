<div align="center">
  <h1>ReposSync</h1>
  <span>English | <a href="./README.zh-CN.md">中文</a></span>
</div>

## ⚡ Introduction

**ReposSync is a tool for batch repository synchronization with the following features:**

- Lightweight: Requires only a GitHub token and a repository list for easy usage.
- Compatibility: Supports syncing multiple source repositories to GitHub with simplified configuration and scheduling.
- Batch Sync: Enables the synchronization of multiple source repositories to target repositories.

## 🚀 Quick Start

```sh
pip install -r requirements.txt
```

### Configuration

1. Copy the .env.example file and rename it to .env
2. Log in to your GitHub account and go to GitHub Settings.
3. Click on "Developer settings" -> "Personal access tokens" -> "Tokens (classic)" -> "Generate new token."
4. Select the necessary permissions: repo, then generate a token and save it.
5. Edit the .env file to configure your GitHub token.
6. Edit the repos.yaml file to set up your repositories.

```yaml
source:
  plat_url: https://git.xxx.com # Source repository platform URL
  username: skylertong # Source repository username
dest:
  plat_url: https://github.com # Target repository platform URL
  username: t8y2 # Target repository username
base_dir: D:\\testrepos # Local directory for storing repositories
repo_list:
  - source_repo_name: repo-1 # First source repository name
    dest_repo_name: repo-1 # Corresponding target repository name (optional, defaults to source name)
    branch: main # Branch
    private: false # Is it a private repository? (optional, default is true, meaning private)
  - source_repo_name: repo-2 # Second source repository name
    branch: main # Branch
```

### Running ReposSync

```shell
python main.py
```
After this, the program will run automatically!

## ✔️ Screenshots

Screenshots will be added later.

## 💕 Appreciate the Star

It's not easy for the project to get stars. If you like this project, please support a star! This is the only motivation for the author to maintain it continuously.


