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

    if response.status_code != 200:
        print(f"Erro ao acessar a API: {response.status_code}")
        print(response.text)
        return []

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

    if not isinstance(repos, list):
        print("❌ Erro ao buscar repositórios. Resposta inesperada da API:")
        print(repos)
        return

    for repo in repos:
        if not isinstance(repo, dict):
            print(f"⚠️ Repositório inesperado no formato: {type(repo)} — {repo}")
            continue

        errors = validate_repo(repo)
        if errors:
            print(f"[{repo['name']}] - Problemas encontrados:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[{repo['name']}] - OK")

if __name__ == "__main__":
    main()
