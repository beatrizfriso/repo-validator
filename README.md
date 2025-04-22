# 🛡️ Repo Validator

Validador automático que garante que os repositórios de uma organização GitHub sigam boas práticas.

## 📋 O que ele verifica?

- Presença de `README.md` e `LICENSE`
- Se a branch principal é `main`
- Se as issues estão habilitadas
- (Opcional) Se possui colaboradores ou tópicos específicos

## ⚙️ Como funciona

Este projeto usa **Python** com a **GitHub API** e é executado automaticamente via **GitHub Actions**, podendo rodar:

- 💠 Manualmente, via GitHub Actions
- ⏰ Automaticamente, com agendamento semanal (`cron`)

## 🚀 Como usar

1. **Clone este repositório.**

2. **Crie dois *Secrets* no GitHub:**

   - `GITHUB_TOKEN`: Token com permissão de leitura nos repositórios
   - `ORG_NAME`: Nome da organização GitHub a ser validada

3. (Opcional) Edite o script `scripts/validate.py` para adicionar mais regras.

4. O GitHub Actions cuidará do resto! Basta ir na aba **Actions** e executar o workflow `Validate Repositories`.

## 📁 Estrutura

repo-validator/ ├── .github/ │ └── workflows/ │ └── validate.yml │ └── validate.py ├── requirements.txt └── README.md

## 📦 Requisitos

- Python 3.10+
- requests (já listado em `requirements.txt`)

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
