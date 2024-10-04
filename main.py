from services.source_repos import SourceRepoManager

if __name__ == "__main__":
    manager = SourceRepoManager("repos.yaml")
    manager.run()

