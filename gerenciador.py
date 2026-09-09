"""Gerenciador de Tarefas (CLI) — módulo principal.

Armazena tarefas em um arquivo JSON local, permitindo adicionar,
listar, concluir e remover tarefas via linha de comando.
"""

import json
from pathlib import Path

ARQUIVO_PADRAO = Path("tarefas.json")


class GerenciadorDeTarefas:
    """Gerencia uma lista de tarefas persistida em JSON."""

    def __init__(self, arquivo=ARQUIVO_PADRAO):
        self.arquivo = Path(arquivo)
        self.tarefas = self._carregar()

    # ------------------------------------------------------------------ #
    # Persistência
    # ------------------------------------------------------------------ #
    def _carregar(self):
        """Carrega as tarefas do arquivo JSON (vazio se não existir)."""
        if not self.arquivo.exists():
            return []
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(dados, list):
            return []
        return dados

    def _salvar(self):
        """Grava a lista de tarefas no arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------ #
    # Operações
    # ------------------------------------------------------------------ #
    def adicionar(self, titulo, concluida=False):
        """Adiciona uma nova tarefa. Retorna a tarefa criada."""
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("O título da tarefa não pode ser vazio.")
        tarefa = {
            "id": self._proximo_id(),
            "titulo": titulo,
            "concluida": concluida,
        }
        self.tarefas.append(tarefa)
        self._salvar()
        return tarefa

    def listar(self, filtro=None):
        """Lista tarefas.

        filtro=None -> todas; 'pendentes' -> não concluídas;
        'concluidas' -> concluídas.
        """
        if filtro == "pendentes":
            return [t for t in self.tarefas if not t["concluida"]]
        if filtro == "concluidas":
            return [t for t in self.tarefas if t["concluida"]]
        return list(self.tarefas)

    def concluir(self, id_tarefa):
        """Marca uma tarefa como concluída. Retorna True/False."""
        for t in self.tarefas:
            if t["id"] == id_tarefa:
                t["concluida"] = True
                self._salvar()
                return True
        return False

    def remover(self, id_tarefa):
        """Remove uma tarefa pelo id. Retorna True/False."""
        tarefa = self._buscar(id_tarefa)
        if tarefa is None:
            return False
        self.tarefas.remove(tarefa)
        self._salvar()
        return True

    # ------------------------------------------------------------------ #
    # Auxiliares
    # ------------------------------------------------------------------ #
    def _buscar(self, id_tarefa):
        for t in self.tarefas:
            if t["id"] == id_tarefa:
                return t
        return None

    def _proximo_id(self):
        if not self.tarefas:
            return 1
        return max(t["id"] for t in self.tarefas) + 1


def resumo(gerenciador):
    """Retorna um resumo (total, pendentes, concluídas)."""
    total = len(gerenciador.listar())
    concluidas = len(gerenciador.listar("concluidas"))
    pendentes = len(gerenciador.listar("pendentes"))
    return {"total": total, "pendentes": pendentes, "concluidas": concluidas}
