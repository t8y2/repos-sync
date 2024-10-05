import requests

from core.config import settings


class GitHubRepoManager:
    @classmethod
    def __init__(cls):
        cls.token = settings['token']['github']
        cls.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {cls.token}',
        }
        cls.github_repos_get_url_prefix = "https://api.github.com/repos/{owner}/{repo}"
        cls.github_repos_create_url = "https://api.github.com/user/repos"

    @classmethod
    def repo_exists(cls, dest_username: str, dest_repo_name: str) -> bool:

        repo_url = cls.github_repos_get_url_prefix.format(owner=dest_username, repo=dest_repo_name)
        response = requests.get(repo_url, headers=cls.headers)
        if response.status_code == 200:
            print(f"查询到Github仓库 '{dest_repo_name}' 已经存在。")
            return True
        return False

    @classmethod
    def create_repo(cls, dest_username: str, dest_repo_name: str, private=True):
        """创建新的 GitHub 仓库。"""
        if cls.repo_exists(dest_username, dest_repo_name):
            print(f"仓库 '{dest_repo_name}' 已经存在, 跳过创建步骤。")
            return
        else:
            print(f"开始创建Github仓库: {dest_repo_name}...")
        data = {
            "name": dest_repo_name,
            "private": private,
        }

        response = requests.post(cls.github_repos_create_url, headers=cls.headers, json=data)

        if response.status_code == 201:
            print(f"成功创建Github仓库: {dest_repo_name}")
        else:
            print(response.status_code)
            print(f"创建Github仓库失败: {response.json()}")


githubManager = GitHubRepoManager()
