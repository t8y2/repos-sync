import inquirer
import requests
from core.config import settings


class ForgejoManager:
    @classmethod
    def __init__(cls):
        cls.token = settings['token']['forgejo']
        cls.headers = {
            'Authorization': f'Bearer {cls.token}',
        }
        cls.list_repos_api = f'{settings["source"]["plat_host"]}/api/v1/user/repos'
        cls.del_repos_api = f'{settings["source"]["plat_host"]}/api/v1/repos/'

    @classmethod
    def list_repos(cls) -> list:
        result = requests.get(cls.list_repos_api, headers=cls.headers)
        if result.status_code == 200:
            return [repo['full_name'] for repo in result.json()]
        else:
            print(result.text)
            return []

    def del_repos(cls) -> None:
        results = cls.list_repos()
        if len(results) == 0:
            print("没有需要删除的仓库")
            return
        while True:
            del_repos = inquirer.prompt([inquirer.Checkbox(
                name="del_repo",
                message="请选择将要删除的仓库",
                choices=results,
            )])['del_repo']
            if len(del_repos) == 0:
                print("请至少选择一个仓库")
            confirm_del = inquirer.prompt([inquirer.Confirm(
                name="confirm_del",
                message=f"确认删除{del_repos}？",
                default=True,
            )])['confirm_del']
            if not confirm_del:
                continue
            else:
                for repo in del_repos:
                    resp = requests.delete(cls.del_repos_api + repo, headers=cls.headers)
                    if resp.status_code == 204:
                        print(f"删除仓库{repo}成功")
                    else:
                        print(f'删除仓库{repo}失败: {resp.text}')
                break


forgejo = ForgejoManager()
