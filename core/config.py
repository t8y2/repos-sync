from typing import Dict, Any

import yaml

config_file = 'config.yaml'


def load_repo_list(filename: str) -> Dict[str, Any]:
    """读取 YAML 文件并返回内容."""
    with open(filename, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


settings = load_repo_list(config_file)
