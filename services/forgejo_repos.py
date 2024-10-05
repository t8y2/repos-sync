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
            return [repo['name'] for repo in result.json()]
        else:
            print(result.text)
            return []


forgejo = ForgejoManager()
