# Gerenciador de Tarefas (CLI)

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
├── gerenciador.py          # módulo principal (regra de negócio)
├── main.py                 # interface de linha de comando (CLI)
├── tests/
│   └── test_gerenciador.py # testes automatizados (pytest)
├── requirements.txt
└── README.md
```

## Fluxo de desenvolvimento

Este projeto usa o fluxo de trabalho com **branches + pull requests**:
as funcionalidades são desenvolvidas em branches separadas (ex.:
`feature/gerenciador-basico`) e integradas à `main` via pull request.

## Autor

Guilherme Panek — [@guilhermepanek-dev](https://github.com/guilhermepanek-dev)
