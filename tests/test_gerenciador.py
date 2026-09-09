"""Testes do Gerenciador de Tarefas (pytest)."""

import json

import pytest

from gerenciador import GerenciadorDeTarefas, resumo


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


# ---------------------------------------------------------------------- #
# Resumo
# ---------------------------------------------------------------------- #
class TestResumo:
    def test_resumo_conta_corretamente(self, gerenciador):
        gerenciador.adicionar("A")
        gerenciador.adicionar("B")
        gerenciador.adicionar("C")
        gerenciador.concluir(1)
        r = resumo(gerenciador)
        assert r == {"total": 3, "pendentes": 2, "concluidas": 1}


# ---------------------------------------------------------------------- #
# Caminho configurável (Docker / variável de ambiente)
# ---------------------------------------------------------------------- #
class TestCaminhoConfiguravel:
    def test_arquivo_via_variavel_de_ambiente(self, tmp_path, monkeypatch):
        destino = tmp_path / "dados" / "tarefas.json"
        destino.parent.mkdir()
        monkeypatch.setenv("TAREFAS_ARQUIVO", str(destino))
        # importar dinamicamente para ler a variável no momento do import
        import importlib

        import gerenciador as modulo

        importlib.reload(modulo)
        gerenciador_local = modulo.GerenciadorDeTarefas()
        gerenciador_local.adicionar("Tarefa no container")
        assert destino.exists()
        assert json.loads(destino.read_text(encoding="utf-8"))[0]["titulo"] == (
            "Tarefa no container"
        )


# ---------------------------------------------------------------------- #
# Semana 6 — novos testes unitários (executados a cada commit de PR)
# ---------------------------------------------------------------------- #
class TestAdicionarCasosExtras:
    def test_adicionar_tarefa_ja_concluida(self, gerenciador):
        tarefa = gerenciador.adicionar("Configurar alertas", concluida=True)
        assert tarefa["concluida"] is True
        assert gerenciador.listar("concluidas") == [tarefa]

    def test_adicionar_titulo_none_dispara_erro(self, gerenciador):
        with pytest.raises(ValueError):
            gerenciador.adicionar(None)

    def test_adicionar_titulo_com_emoji_e_unicode(self, gerenciador):
        tarefa = gerenciador.adicionar("🐳 Dockerizar a aplicação")
        assert tarefa["titulo"] == "🐳 Dockerizar a aplicação"
        recarregado = GerenciadorDeTarefas(arquivo=gerenciador.arquivo)
        assert recarregado.listar()[0]["titulo"] == "🐳 Dockerizar a aplicação"

    def test_adicionar_titulo_muito_longo_e_aceito(self, gerenciador):
        longo = "DevOps" * 50  # 300 caracteres, sem espaços nas pontas
        tarefa = gerenciador.adicionar(longo)
        assert tarefa["titulo"] == longo


class TestRemover:
    def test_remover_tarefa_existente(self, gerenciador):
        gerenciador.adicionar("Tarefa 1")
        gerenciador.adicionar("Tarefa 2")
        assert gerenciador.remover(1) is True
        titulos = [t["titulo"] for t in gerenciador.listar()]
        assert titulos == ["Tarefa 2"]

    def test_remover_tarefa_inexistente_retorna_false(self, gerenciador):
        assert gerenciador.remover(42) is False

    def test_proximo_id_apos_remover_usa_maior_id_restante(self, gerenciador):
        gerenciador.adicionar("A")  # id 1
        gerenciador.adicionar("B")  # id 2
        gerenciador.remover(2)      # resta apenas o id 1
        nova = gerenciador.adicionar("C")
        # _proximo_id() = maior id restante + 1 = 2
        assert nova["id"] == 2


class TestBordasPersistencia:
    def test_arquivo_com_json_valido_mas_nao_lista(self, tmp_path):
        arquivo = tmp_path / "tarefas.json"
        arquivo.write_text('{"tarefas": "não é lista"}', encoding="utf-8")
        gerenciador = GerenciadorDeTarefas(arquivo=arquivo)
        assert gerenciador.listar() == []

    def test_listar_retorna_copia_da_lista_interna(self, gerenciador):
        gerenciador.adicionar("Original")
        copia = gerenciador.listar()
        copia.append({"id": 99, "titulo": "Intrusa", "concluida": False})
        assert len(gerenciador.listar()) == 1


class TestResumoCasosExtras:
    def test_resumo_sem_tarefas(self, gerenciador):
        assert resumo(gerenciador) == {"total": 0, "pendentes": 0, "concluidas": 0}

    def test_concluir_persiste_no_disco(self, gerenciador, tmp_path):
        gerenciador.adicionar("Escrever testes unitários")
        gerenciador.concluir(1)
        novo = GerenciadorDeTarefas(arquivo=tmp_path / "tarefas.json")
        assert novo.listar()[0]["concluida"] is True

    def test_concluir_duas_vezes_mantem_concluida(self, gerenciador):
        gerenciador.adicionar("Merge na main")
        assert gerenciador.concluir(1) is True
        assert gerenciador.concluir(1) is True  # idempotente
        assert gerenciador.listar()[0]["concluida"] is True
