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
    
    # Validando Issues
    if not repo.get("has_issues", False):
        errors.append("Issues desabilitadas")
    
    # Validando branch principal
    if repo.get("default_branch") != "main":
        errors.append("Branch principal não é 'main'")
    
    # Validando README
    readme_url = f"{repo['url']}/contents/README.md"
    readme_resp = requests.get(readme_url, headers=headers)
    if readme_resp.status_code != 200:
        errors.append("Sem README.md")
    
    # Validando LICENSE
    license_url = f"{repo['url']}/contents/LICENSE"
    license_resp = requests.get(license_url, headers=headers)
    if license_resp.status_code != 200:
        errors.append("Sem LICENSE")
    
    # Verificando visibilidade (público ou privado)
    visibility = "🌐 Público" if not repo.get("private", False) else "🔒 Privado"
    
    # Verificando actions configuradas
    actions_url = f"{repo['url']}/actions/workflows"
    actions_resp = requests.get(actions_url, headers=headers)
    actions_status = "⚙️ Actions ativas" if actions_resp.status_code == 200 and actions_resp.json().get('total_count', 0) > 0 else "⚠️ Nenhuma action"
    
    # Verificando presença de testes
    contents_url = f"{repo['url']}/contents"
    contents_resp = requests.get(contents_url, headers=headers)
    has_tests = "❌ Sem testes"
    if contents_resp.status_code == 200:
        items = [item['name'].lower() for item in contents_resp.json()]
        if 'tests' in items or any(name.startswith('test') for name in items):
            has_tests = "🧪 Testes encontrados"
    
    return errors, visibility, actions_status, has_tests

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
    private_count = 0
    public_count = 0
    total_repos = len(repos)
    valid_repos = 0
    invalid_repos = 0

    for repo in repos:
        if not isinstance(repo, dict):
            continue
        errors, visibility, actions_status, has_tests = validate_repo(repo)
        if errors:
            failed[repo['name']] = {
                "errors": errors,
                "visibility": visibility,
                "actions_status": actions_status,
                "has_tests": has_tests,
            }
            invalid_repos += 1
        else:
            passed.append(repo['name'])
            valid_repos += 1

        # Contagem de visibilidade
        if repo.get("private", False):
            private_count += 1
        else:
            public_count += 1

    # Estatísticas gerais
    report_lines.append("### Estatísticas Gerais")
    report_lines.append(f"- Total de repositórios: {total_repos}")
    report_lines.append(f"- Repositórios válidos: {valid_repos} ✅")
    report_lines.append(f"- Repositórios com problemas: {invalid_repos} ❌")
    report_lines.append(f"- Repositórios privados: {private_count} 🔒")
    report_lines.append(f"- Repositórios públicos: {public_count} 🌐\n")

    # Listagem de repositórios
    if passed:
        report_lines.append("✅ Repositórios sem problemas:")
        for name in passed:
            report_lines.append(f"- {name}")
        report_lines.append("")

    if failed:
        report_lines.append("❌ Repositórios com problemas:")
        for name, details in failed.items():
            report_lines.append(f"- {name}")
            for error in details["errors"]:
                report_lines.append(f"  - {error}")
            report_lines.append(f"  - Visibilidade: {details['visibility']}")
            report_lines.append(f"  - Actions Status: {details['actions_status']}")
            report_lines.append(f"  - Testes: {details['has_tests']}")
        report_lines.append("")

    report_lines.append(f"📅 Última execução: {datetime.utcnow().strftime('%d/%m/%Y %H:%M UTC')}\n")

    # Escrever relatório
    with open("validation_report.md", "w") as report:
        report.write("\n".join(report_lines))

    # Exibir no console
    print("\n".join(report_lines))


if __name__ == "__main__":
    main()
