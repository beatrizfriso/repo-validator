import requests
import os
from datetime import datetime

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

    report_lines = []
    report_lines.append(f"# 📋 Validação de Repositórios — {ORG_NAME}\n")

    passed = []
    failed = {}

    for repo in repos:
        if not isinstance(repo, dict):
            continue
        errors = validate_repo(repo)
        if errors:
            failed[repo['name']] = errors
        else:
            passed.append(repo['name'])

    if passed:
        report_lines.append("✅ Repositórios sem problemas:")
        for name in passed:
            report_lines.append(f"- {name}")
        report_lines.append("")

    if failed:
        report_lines.append("❌ Repositórios com problemas:")
        for name, errs in failed.items():
            report_lines.append(f"- {name}")
            for err in errs:
                report_lines.append(f"  - {err}")
        report_lines.append("")

    report_lines.append(f"📅 Última execução: {datetime.utcnow().strftime('%d/%m/%Y %H:%M UTC')}\n")

    with open("validation_report.md", "w") as report:
        report.write("\n".join(report_lines))

    print("\n".join(report_lines))

if __name__ == "__main__":
    main()
