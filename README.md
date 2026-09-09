# Gerenciador de Tarefas (CLI)

![CI](https://github.com/guilhermepanek-dev/gerenciador-tarefas/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/guilhermepanek-dev/gerenciador-tarefas/actions/workflows/cd.yml/badge.svg)

Projeto desenvolvido durante a disciplina de DevOps para praticar o fluxo
completo de CI/CD com GitHub.

Um gerenciador de tarefas simples em **Python**, executado pela linha de
comando, com armazenamento local em JSON e testes automatizados com **pytest**.

## Funcionalidades

- Adicionar tarefas com título
- Listar todas as tarefas
- Filtrar por pendentes / concluídas
- Marcar tarefas como concluídas
- Remover tarefas
- Resumo com estatísticas (total, pendentes, concluídas)

## CI/CD (GitHub Actions)

Este repositório possui dois workflows automatizados:

- **CI (`.github/workflows/ci.yml`)** — dispara em pushes para a `main` e em
  pull requests:
  - **Lint (code quality):** análise estática com [Ruff](https://docs.astral.sh/ruff/);
  - **Testes:** matriz de pytest nas versões 3.10, 3.11 e 3.12 do Python.

- **CD (`.github/workflows/cd.yml`)** — valida o **build** do pacote
  (sdist + wheel) em pull requests e, no merge para a `main`, publica os
  artefatos como **GitHub Release** (continuous deployment).

## Requisitos

- Python 3.10+
- pytest (para executar os testes)

## Como usar

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Adicionar tarefas
python main.py adicionar "Estudar fluxo de CI/CD"
python main.py adicionar "Criar pull request"

# Listar tarefas
python main.py listar
python main.py listar --filtro pendentes
python main.py listar --filtro concluidas

# Concluir e remover
python main.py concluir 1
python main.py remover 2

# Resumo
python main.py resumo
```

## Como executar os testes

```bash
python -m pytest tests/ -v
```

## Estrutura do projeto

```
gerenciador-tarefas/
├── .github/
│   └── workflows/
│       ├── ci.yml          # workflow de CI (lint + testes)
│       └── cd.yml          # workflow de CD (build + release)
├── gerenciador.py          # módulo principal (regra de negócio)
├── main.py                 # interface de linha de comando (CLI)
├── tests/
│   └── test_gerenciador.py # testes automatizados (pytest)
├── pyproject.toml          # configuração de build do pacote
├── requirements.txt
└── README.md
```

## Fluxo de desenvolvimento

Este projeto usa o fluxo de trabalho com **branches + pull requests**:
as funcionalidades são desenvolvidas em branches separadas (ex.:
`feature/gerenciador-basico`) e integradas à `main` via pull request, com os
workflows de CI e CD validando cada mudança automaticamente.

## Autor

Guilherme Panek — [@guilhermepanek-dev](https://github.com/guilhermepanek-dev)
