# Gerenciador de Tarefas (CLI)

Projeto desenvolvido durante a disciplina de DevOps para praticar o fluxo
completo de CI/CD com GitHub.

Um gerenciador de tarefas simples em **Python**, executado pela linha de
comando, com armazenamento local em JSON e testes automatizados com **pytest**.

## Funcionalidades (planejadas)

- Adicionar tarefas com título
- Listar todas as tarefas
- Filtrar por pendentes / concluídas
- Marcar tarefas como concluídas
- Remover tarefas
- Resumo com estatísticas

## Requisitos

- Python 3.10+
- pytest (para executar os testes)

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
│   └── test_gerenciador.py # testes automatizados
├── requirements.txt
└── README.md
```

## Autor

Guilherme Panek — [@guilhermepanek-dev](https://github.com/guilhermepanek-dev)
