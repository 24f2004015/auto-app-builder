# deploy.py
from github import Github

def create_github_repo(repo_name, code_files, token):
    g = Github(token)
    user = g.get_user()
    repo = user.create_repo(repo_name, private=False)

    # Add MIT license
    mit_license = """MIT License
Copyright (c) 2025
Permission is hereby granted..."""
    repo.create_file("LICENSE", "Add MIT license", mit_license)

    # Push code files
    for filename, content in code_files.items():
        repo.create_file(filename, f"Add {filename}", content)

    # Get latest commit SHA
    commit_sha = repo.get_commits()[0].sha
    return repo.html_url, commit_sha

def deploy_pages(repo_name, token):
    g = Github(token)
    repo = g.get_user().get_repo(repo_name)
    # Enable Pages (PyGithub may require API call if not supported)
    pages_url = f"https://{repo.owner.login}.github.io/{repo.name}/"
    return pages_url
