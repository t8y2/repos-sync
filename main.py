import inquirer

from services.forgejo_repos import forgejo
from services.github_repos import github
from services.source_repos import source_manager

if __name__ == "__main__":
    print("Starting...")
    choice = inquirer.prompt([inquirer.List(
        name="choice",
        message="请选择使用的功能",
        choices=['批量同步', '批量删除'],
    )])['choice']
    if choice == '批量同步':
        source_manager.run()
    elif choice == '批量删除':
        choice_platform = inquirer.prompt([inquirer.List(
            name="choice_platform",
            message="请选择使用的平台",
            choices=['forgejo', 'github'],
        )])['choice_platform']
        if choice_platform == 'forgejo':
            forgejo.del_repos()
        if choice_platform == 'github':
            github.del_repos()
