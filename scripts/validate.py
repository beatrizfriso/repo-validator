import requests
import os

GITHUB_API = "https://api.github.com"
ORG_NAME = os.getenv("ORG_NAME")
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repositories():
    url = f"{GITHUB_API}/orgs/{ORG_NAME}/repos"
    response = requests.get(url, headers=headers)
    return response.json()

def validate_repo(repo):
    errors = []
    if not repo.get("has_issues", False):
        errors.append("Issues desabilitadas")
    if repo.get("default_branch") != "main":
        errors.append("Branch principal não é 'main'")
    return errors

def main():
    repos = get_repositories()
    for repo in repos:
        errors = validate_repo(repo)
        if errors:
            print(f"[{repo['name']}] - Problemas encontrados:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[{repo['name']}] - OK")

if __name__ == "__main__":
    main()
