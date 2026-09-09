"""Testes do Gerenciador de Tarefas (pytest)."""

import json

import pytest

from gerenciador import GerenciadorDeTarefas


@pytest.fixture
def gerenciador(tmp_path):
    """Retorna um gerenciador apontando para um arquivo temporário."""
    return GerenciadorDeTarefas(arquivo=tmp_path / "tarefas.json")


# ---------------------------------------------------------------------- #
# Adicionar
# ---------------------------------------------------------------------- #
class TestAdicionar:
    def test_adicionar_primeira_tarefa(self, gerenciador):
        tarefa = gerenciador.adicionar("Estudar DevOps")
        assert tarefa["id"] == 1
        assert tarefa["titulo"] == "Estudar DevOps"
        assert tarefa["concluida"] is False
        assert len(gerenciador.listar()) == 1

    def test_adicionar_varias_tarefas_incrementa_ids(self, gerenciador):
        gerenciador.adicionar("Tarefa A")
        gerenciador.adicionar("Tarefa B")
        gerenciador.adicionar("Tarefa C")
        ids = [t["id"] for t in gerenciador.listar()]
        assert ids == [1, 2, 3]

    def test_adicionar_titulo_vazio_dispara_erro(self, gerenciador):
        with pytest.raises(ValueError):
            gerenciador.adicionar("   ")

    def test_titulo_com_espacos_e_normalizado(self, gerenciador):
        tarefa = gerenciador.adicionar("  Aprender CI/CD  ")
        assert tarefa["titulo"] == "Aprender CI/CD"


# ---------------------------------------------------------------------- #
# Persistência
# ---------------------------------------------------------------------- #
class TestPersistencia:
    def test_tarefas_salvas_em_disco(self, gerenciador, tmp_path):
        gerenciador.adicionar("Estudar CI/CD")
        conteudo = json.loads((tmp_path / "tarefas.json").read_text(encoding="utf-8"))
        assert conteudo == [
            {"id": 1, "titulo": "Estudar CI/CD", "concluida": False}
        ]

    def test_recarregar_mantem_estado(self, gerenciador, tmp_path):
        gerenciador.adicionar("Escrever testes")
        novo = GerenciadorDeTarefas(arquivo=tmp_path / "tarefas.json")
        assert novo.listar()[0]["titulo"] == "Escrever testes"

    def test_arquivo_corrompido_nao_quebra_aplicacao(self, tmp_path):
        arquivo = tmp_path / "tarefas.json"
        arquivo.write_text("isto não é JSON válido", encoding="utf-8")
        gerenciador = GerenciadorDeTarefas(arquivo=arquivo)
        assert gerenciador.listar() == []


