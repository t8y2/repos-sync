import inquirer
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
        cls.github_repos_list_url = "https://api.github.com/user/repos"  # 获取用户仓库列表的URL
        cls.github_repos_delete_url = "https://api.github.com/repos/{fullname}"

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

    @classmethod
    def list_repos(cls) -> list:
        """获取 GitHub 用户的所有仓库列表"""
        response = requests.get(cls.github_repos_list_url, headers=cls.headers)
        if response.status_code == 200:
            repos = response.json()
            repo_full_names = [repo['full_name'] for repo in repos]
            print(f"获取到 {len(repo_full_names)} 个仓库")
            return repo_full_names
        else:
            print(f"获取仓库列表失败: {response.status_code}")
            return []

    @classmethod
    def del_repos(cls) -> None:
        """删除指定的 GitHub 仓库"""
        repos_fullname_list = cls.list_repos()
        while True:
            dest_repos_fullname = inquirer.prompt([inquirer.Checkbox(
                name="dest_repos_fullname",
                message="请选择要删除的仓库",
                choices=repos_fullname_list,
            )])['dest_repos_fullname']
            if len(dest_repos_fullname) == 0:
                print("请至少选择一个仓库")
            confirm_del = inquirer.prompt([inquirer.Confirm(
                name="confirm_del",
                message=f"确认删除{dest_repos_fullname}？",
                default=True,
            )])['confirm_del']
            if not confirm_del:
                continue
            else:
                for dest_repo_fullname in dest_repos_fullname:
                    response = requests.delete(cls.github_repos_delete_url.format(fullname=dest_repo_fullname), headers=cls.headers)
                    if response.status_code == 204:
                        print(f"成功删除Github仓库: {dest_repo_fullname}")
                    else:
                        print(f"删除仓库{dest_repo_fullname}失败: {response.status_code} - {response.json()}")
                break


github = GitHubRepoManager()
