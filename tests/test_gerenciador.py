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


# ---------------------------------------------------------------------- #
# Listar / filtrar
# ---------------------------------------------------------------------- #
class TestListar:
    def test_listar_vazio(self, gerenciador):
        assert gerenciador.listar() == []

    def test_filtro_pendentes(self, gerenciador):
        gerenciador.adicionar("Pendente 1")
        gerenciador.adicionar("Pendente 2")
        gerenciador.concluir(1)
        pendentes = gerenciador.listar("pendentes")
        assert len(pendentes) == 1
        assert pendentes[0]["titulo"] == "Pendente 2"

    def test_filtro_concluidas(self, gerenciador):
        gerenciador.adicionar("Tarefa 1")
        gerenciador.adicionar("Tarefa 2")
        gerenciador.concluir(2)
        concluidas = gerenciador.listar("concluidas")
        assert len(concluidas) == 1
        assert concluidas[0]["id"] == 2


# ---------------------------------------------------------------------- #
# Concluir
# ---------------------------------------------------------------------- #
class TestConcluir:
    def test_concluir_tarefa_existente(self, gerenciador):
        gerenciador.adicionar("Fazer o PR")
        assert gerenciador.concluir(1) is True
        assert gerenciador.listar()[0]["concluida"] is True

    def test_concluir_tarefa_inexistente(self, gerenciador):
        assert gerenciador.concluir(999) is False


