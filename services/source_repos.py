import yaml
import subprocess
import os
from typing import List, Dict, Any


class SourceRepoManager:
    @classmethod
    def __init__(cls, config_file: str):
        """初始化 RepoManager，加载配置文件."""
        cls.config = cls.load_repo_list(config_file)
        cls.source_repo_prefix = cls.config['source_repo_prefix']
        cls.repo_list = cls.config['repo_list']
        cls.base_dir = cls.config['base_dir']

        # 确保存放仓库的目录存在
        os.makedirs(cls.base_dir, exist_ok=True)

    @staticmethod
    def load_repo_list(filename: str) -> Dict[str, Any]:
        """读取 YAML 文件并返回内容."""
        with open(filename, 'r') as file:
            return yaml.safe_load(file)

    @classmethod
    def sync_repo(cls, repo_name: str, branch: str) -> None:
        """克隆或拉取指定的仓库."""
        repo_url = f"{cls.source_repo_prefix}{repo_name}"
        repo_dir = os.path.join(cls.base_dir, repo_name.split("/")[-1])  # 仓库目录

        if os.path.exists(repo_dir):
            # 如果仓库已经存在，则拉取最新代码
            print(f"本地检测到仓库 {repo_name} ,正在拉取最新代码...")
            subprocess.run(["git", "pull", "origin", branch], check=True, cwd=repo_dir)
            print(f"仓库 {repo_name} 已成功更新。")
        else:
            # 如果仓库不存在，则克隆
            print(f"检测到仓库 {repo_name} 不存在,正在克隆...")
            subprocess.run(["git", "clone", "-b", branch, repo_url], check=True, cwd=cls.base_dir)
            print(f"仓库 {repo_name} 已成功克隆。")

    @classmethod
    def set_remote_url(cls, repo_dir: str, remote_url: str) -> None:
        """设置远程仓库 URL."""
        if os.path.exists(repo_dir):
            try:
                subprocess.run(
                    ["git", "remote", "set-url", "--add", "origin", remote_url],
                    check=True,
                    cwd=repo_dir
                )
                print(f"成功为 {repo_dir} 添加远程仓库 {remote_url}。")
            except subprocess.CalledProcessError as e:
                print(f"设置远程仓库失败: {e}")
        else:
            print(f"仓库目录 {repo_dir} 不存在。")

    @classmethod
    def push_code(cls, repo_dir: str, branch: str) -> None:
        """强制推送代码到远程仓库."""
        if os.path.exists(repo_dir):
            try:
                # 切换到指定分支
                print(f"切换到分支 {branch}...")
                subprocess.run(
                    ["git", "checkout", branch],
                    check=True,
                    cwd=repo_dir
                )
                print(f"成功切换到分支 {branch}。")

                # 强制推送代码到远程仓库
                print(f"正在推送代码到远程仓库的分支 {branch}...")
                subprocess.run(
                    ["git", "push", "-f", "origin", branch],
                    check=True,
                    cwd=repo_dir
                )
                print(f"代码成功推送到远程仓库的分支 {branch}。")
            except subprocess.CalledProcessError as e:
                print(f"推送代码失败: {e}")
        else:
            print(f"仓库目录 {repo_dir} 不存在。")

    @classmethod
    def run(cls) -> None:
        """同步每个仓库."""
        for repo in cls.repo_list:
            repo_name = repo['name']
            branch = repo['branch']
            remote_url = f"{cls.source_repo_prefix}{repo_name}"  # 远程仓库 URL
            repo_dir = str(os.path.join(cls.base_dir, repo_name.split("/")[-1]))  # 仓库目录
            cls.sync_repo(repo_name, branch)  # 拉取或克隆仓库
            cls.set_remote_url(repo_dir, remote_url)  # 设置远程仓库 URL（假设 remote_url 是从配置中获取）
            # cls.push_code(repo_dir, branch)  # 推送代码


if __name__ == "__main__":
    manager = SourceRepoManager("../repos.yaml")
    manager.run()
