import subprocess
import os
import inquirer
from core.config import settings
from services.forgejo_repos import forgejo
from services.github_repos import github


class SourceRepoManager:
    def __init__(self) -> None:
        """初始化 RepoManager，加载配置文件."""
        self.source_host = settings['source']['plat_host']
        self.dest_host = settings['dest']['plat_host']
        self.repo_list = settings['repo_list']
        self.base_dir = settings['base_dir']
        os.makedirs(self.base_dir, exist_ok=True)

    def select_platform(self) -> str:
        """选择源端平台"""
        return inquirer.prompt([inquirer.List(
            "platform",
            message="请选择源端仓库使用的平台",
            choices=["forgejo", "github", "手动配置"],
        )])['platform']

    def select_repos(self, platform: str) -> tuple:
        """选择源端仓库和可见性设置"""
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

    def sync_repo(self, repo_full_name: str, repo_dir: str, branch: str = None) -> None:
        """克隆或拉取指定的仓库."""
        repo_url = f"{self.source_host}/{repo_full_name}"
        if branch:
            self.run_git_command(repo_dir, ["git", "pull", "origin", branch], "拉取最新代码", repo_url)
        else:
            self.run_git_command(repo_dir, ["git", "pull"], "拉取最新代码", repo_url)

    def set_remote_url(self, repo_dir: str, remote_url: str) -> None:
        """设置远程仓库 URL."""
        if not self.check_if_repo_exists(repo_dir):
            return
        remotes = self.run_git_command(repo_dir, ["git", "remote", "-v"], "获取远程仓库", capture_output=True)
        if remote_url not in remotes:
            self.run_git_command(repo_dir, ["git", "remote", "set-url", "--add", "origin", remote_url], "添加远程仓库",
                                 remote_url)

    def push_code(self, repo_dir: str, branch: str = None) -> None:
        """推送代码到远程仓库."""
        if branch:
            self.run_git_command(repo_dir, ["git", "checkout", branch], f"切换到分支 {branch}")
            self.run_git_command(repo_dir, ["git", "push", "-f", "origin", branch], f"推送代码到分支 {branch}")
        else:
            self.run_git_command(repo_dir, ["git", "push", "-f"], "推送代码到默认分支")
            print("推送完成。")

    def run_git_command(self, repo_dir: str, command: list, action: str, repo_url: str = None,
                        capture_output: bool = False) -> str:
        """执行 Git 命令."""
        if repo_url and not os.path.exists(repo_dir):
            print(f"{action}：克隆仓库 {repo_url} 到 {repo_dir}...")
            subprocess.run(["git", "clone", repo_url], cwd=self.base_dir, check=True)
        else:
            print(f"正在 {action} ...")
            result = subprocess.run(command, cwd=repo_dir, check=True, text=True,
                                    stdout=subprocess.PIPE if capture_output else None)
            if capture_output:
                return result.stdout

    def check_if_repo_exists(self, repo_dir: str) -> bool:
        """检查仓库是否存在."""
        if not os.path.exists(repo_dir):
            print(f"仓库目录 {repo_dir} 不存在。")
            return False
        return True

    def run(self) -> None:
        """主运行函数"""
        platform = self.select_platform()
        repos_full_names, visibility = self.select_repos(platform)

        if repos_full_names:
            for i, repo_name in enumerate(repos_full_names, start=1):
                self.process_auto_repo(repo_name, visibility, i)
            return
        else:
            # 读取配置文件批量处理 repo_list
            for i, repo in enumerate(self.repo_list, start=1):
                self.process_manual_repo(repo['source_repo_name'], repo.get('private', True), i)

    def process_manual_repo(self, repo_name: str, visibility: str, index: int) -> None:
        """处理每个仓库"""
        print(f"##################### 正在处理第 {index} 个仓库: {repo_name} #####################")
        repo_dir = os.path.join(self.base_dir, repo_name)
        source_repo_full_name = f"{settings['source']['username']}/{repo_name}"
        dest_repo_full_name = f"{settings['dest']['username']}/{repo_name}"
        dest_remote_url = f"{self.dest_host}/{dest_repo_full_name}"
        self.sync_repo(source_repo_full_name, repo_dir)
        self.set_remote_url(repo_dir, dest_remote_url)
        githubManager.create_repo(settings['dest']['username'], repo_name, visibility)
        self.push_code(repo_dir)
        print(f"第 {index} 个仓库处理完毕。\n\n")

    def process_auto_repo(self, repo_full_name: str, visibility: str, index: int) -> None:
        """处理每个仓库"""
        repo_name = repo_full_name.split('/')[-1]
        print(f"##################### 正在处理第 {index} 个仓库: {repo_name} #####################")
        repo_dir = os.path.join(self.base_dir, repo_name)
        dest_remote_url = f"{self.dest_host}/{settings['dest']['username']}/{repo_name}"
        self.sync_repo(repo_full_name, repo_dir)
        self.set_remote_url(repo_dir, dest_remote_url)
        githubManager.create_repo(settings['dest']['username'], repo_name, visibility)
        self.push_code(repo_dir)
        print(f"第 {index} 个仓库处理完毕。\n\n")


source_manager = SourceRepoManager()
