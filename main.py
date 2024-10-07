import inquirer

from services.forgejo_repos import forgejo
from services.source_repos import SourceRepoManager, source_manager

if __name__ == "__main__":
    print("Starting...")
    choice = inquirer.prompt([inquirer.List(
        name="choice",
        message="请选择使用的功能",
        choices=['批量同步', '批量删除(仅支持forgejo)'],
    )])['choice']
    if choice == '批量同步':
        source_manager.run()
    elif choice == '批量删除(仅支持forgejo)':
        forgejo.del_repos()

