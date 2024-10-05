import os

import requests
from dotenv import load_dotenv

from core.config import settings


class ForgejoManager:
    @classmethod
    def __init__(cls):
        cls.token = settings['token']['forgejo']
        cls.headers = {
            'Authorization': f'Bearer {cls.token}',
        }
        cls.list_repos_api = f'{settings["source"]["plat_host"]}/api/v1/user/repos'

    @classmethod
    def list_repos(cls) -> list:
        result = requests.get(cls.list_repos_api, headers=cls.headers)
        if result.status_code == 200:
            return result.json()
        else:
            print(result.text)
            return []


forgejo = ForgejoManager()

if __name__ == '__main__':
    repos = forgejo.list_repos()
    for repo in repos:
        print(repo['full_name'])
        print(repo['clone_url'])

