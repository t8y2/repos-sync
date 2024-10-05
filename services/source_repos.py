import subprocess
import os

import inquirer

from core.config import settings
from services.forgejo_repos import forgejo
from services.github_repos import githubManager


class SourceRepoManager:
    supported_platforms = ["forgejo", "gitlab", "github"]

    @classmethod
    def __init__(cls):
        """初始化 RepoManager，加载配置文件."""
        cls.source_url_prefix = f"{settings['source']['plat_host']}/{settings['source']['username']}"
        cls.dest_url_prefix = f"{settings['dest']['plat_host']}/{settings['dest']['username']}"
        cls.repo_list = settings['repo_list']
        cls.base_dir = settings['base_dir']
        # 确保存放仓库的目录存在
        os.makedirs(cls.base_dir, exist_ok=True)

        selected_source_repos_names, default_visibility = cls.select_steps()

    @classmethod
    def select_steps(cls):
        platform = inquirer.prompt([inquirer.List(
            "platform",
            message="请选择源端仓库使用的平台",
            choices=["forgejo", "github", "手动配置"],
        )])['platform']

        if platform == "forgejo":
            source_repos_names = forgejo.list_repos()
            selected_source_repos_names = inquirer.prompt([inquirer.Checkbox(
                "names",
                message="请选择要进行同步的源端仓库",
                choices=source_repos_names,
            )])['names']
            default_visibility = inquirer.prompt([inquirer.List(
                "visibility",
                message="请选择仓库的统一访问权限",
                choices=["public", "private"],
            )])['visibility']
            return selected_source_repos_names, default_visibility
        return [], "public"

    @classmethod
    def sync_repo(cls, repo_name: str, repo_dir: str, branch: str = "main") -> None:
        """克隆或拉取指定的仓库."""
        repo_url = f"{cls.source_url_prefix}/{repo_name}"
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
        """设置远程仓库 URL，如果 URL 已存在则不重复添加。"""
        if os.path.exists(repo_dir):
            try:
                # 获取当前仓库的所有远程 URL
                remotes = subprocess.run(
                    ["git", "remote", "-v"],
                    check=True,
                    cwd=repo_dir,
                    text=True,
                    stdout=subprocess.PIPE
                ).stdout.splitlines()

                # 检查远程 URL 是否已经存在
                remote_exists = any(remote_url in remote for remote in remotes)

                if not remote_exists:
                    # 如果远程 URL 不存在，则添加
                    subprocess.run(
                        ["git", "remote", "set-url", "--add", "origin", remote_url],
                        check=True,
                        cwd=repo_dir
                    )
                    print(f"成功为 {repo_dir} 添加远程仓库 {remote_url}。")
                else:
                    print(f"远程仓库 {remote_url} 已存在，无需重复添加。")
            except subprocess.CalledProcessError as e:
                print(f"设置远程仓库失败: {e}")
        else:
            print(f"仓库目录 {repo_dir} 不存在。")

    @classmethod
    def push_code(cls, repo_dir: str, branch: str = "main") -> None:
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
        repos_names, visibility = cls.select_steps
        if repos_names:
            for i, repo_name in enumerate(repos_names, start=1):
                print(f"##################### 正在处理第 {i} 个仓库: {repo_name} #####################")
                dest_remote_url = f"{cls.dest_url_prefix}/{repo_name}"
                repo_dir = str(os.path.join(cls.base_dir, repo_name))  # 仓库目录
                cls.sync_repo(repo_name, repo_dir)  # 拉取或克隆仓库
                cls.set_remote_url(repo_dir, dest_remote_url)  # 设置远程仓库 URL（假设 remote_url 是从配置中获取）
                githubManager.create_repo(settings['dest']['username'], repo_name, visibility)
                cls.push_code(repo_dir)  # 推送代码
                print(f"第 {i} 个仓库处理完毕。\n\n")
            return

        """同步每个仓库."""
        for i, repo in enumerate(cls.repo_list, start=1):
            print(f"##################### 正在处理第 {i} 个仓库: {repo['source_repo_name']} #####################")
            source_repo_name = repo['source_repo_name']
            branch = repo['branch']
            is_repo_private = repo['private'] if 'private' in repo else True
            dest_repo_name = repo['dest_repo_name'] if 'dest_repo_name' in repo else source_repo_name  # 默认使用源仓库名
            dest_remote_url = f"{cls.dest_url_prefix}/{dest_repo_name}"
            repo_dir = str(os.path.join(cls.base_dir, source_repo_name))  # 仓库目录
            cls.sync_repo(source_repo_name, repo_dir, branch)  # 拉取或克隆仓库
            cls.set_remote_url(repo_dir, dest_remote_url)  # 设置远程仓库 URL（假设 remote_url 是从配置中获取）
            githubManager.create_repo(settings['dest']['username'], dest_repo_name, is_repo_private)
            cls.push_code(repo_dir, branch)  # 推送代码
            print(f"第 {i} 个仓库处理完毕。\n\n")


source = SourceRepoManager()

if __name__ == "__main__":
    source.select_steps()
