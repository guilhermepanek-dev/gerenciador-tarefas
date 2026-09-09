"""Interface de linha de comando (CLI) do Gerenciador de Tarefas.

Uso:
    python main.py adicionar "Título da tarefa"
    python main.py listar [--filtro pendentes|concluidas]
    python main.py concluir <id>
    python main.py remover <id>
    python main.py resumo
"""

import argparse
import sys

from gerenciador import GerenciadorDeTarefas, resumo


def montar_parser():
    parser = argparse.ArgumentParser(
        prog="gerenciador",
        description="Gerenciador de tarefas via linha de comando.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("adicionar", help="Adiciona uma nova tarefa.")
    p_add.add_argument("titulo", help="Título da tarefa.")

    p_list = sub.add_parser("listar", help="Lista as tarefas.")
    p_list.add_argument(
        "--filtro",
        choices=["pendentes", "concluidas"],
        default=None,
        help="Filtra por pendentes ou concluídas.",
    )

    p_concluir = sub.add_parser("concluir", help="Conclui uma tarefa pelo id.")
    p_concluir.add_argument("id", type=int, help="Id da tarefa.")

    p_remover = sub.add_parser("remover", help="Remove uma tarefa pelo id.")
    p_remover.add_argument("id", type=int, help="Id da tarefa.")

    sub.add_parser("resumo", help="Exibe um resumo das tarefas.")

    return parser


def formatar_tarefa(t):
    marca = "x" if t["concluida"] else " "
    return f"[{marca}] #{t['id']} — {t['titulo']}"


def main(argv=None):
    parser = montar_parser()
    args = parser.parse_args(argv)
    ger = GerenciadorDeTarefas()

    if args.comando == "adicionar":
        try:
            tarefa = ger.adicionar(args.titulo)
        except ValueError as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            return 1
        print(f"Tarefa criada: {formatar_tarefa(tarefa)}")
        return 0

    if args.comando == "listar":
        tarefas = ger.listar(args.filtro)
        if not tarefas:
            print("Nenhuma tarefa encontrada.")
            return 0
        for t in tarefas:
            print(formatar_tarefa(t))
        return 0

    if args.comando == "concluir":
        if ger.concluir(args.id):
            print(f"Tarefa #{args.id} concluída!")
            return 0
        print(f"Erro: tarefa #{args.id} não encontrada.", file=sys.stderr)
        return 1

    if args.comando == "remover":
        if ger.remover(args.id):
            print(f"Tarefa #{args.id} removida.")
            return 0
        print(f"Erro: tarefa #{args.id} não encontrada.", file=sys.stderr)
        return 1

    if args.comando == "resumo":
        r = resumo(ger)
        print(
            f"Total: {r['total']} | "
            f"Pendentes: {r['pendentes']} | "
            f"Concluídas: {r['concluidas']}"
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
