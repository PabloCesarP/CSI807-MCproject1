"""Impacto de escolhas acadêmicas. Linguagem neutra: mostra relações, não decide."""
from __future__ import annotations

from dataclasses import replace

from .aluno import AlunoDemo
from .matriz import Matriz
from .status import Status, status

# Decisão de projeto (não vem dos prints): a partir de quantas disciplinas
# pendentes dependentes uma disciplina é sinalizada como possível gargalo.
LIMITE_GARGALO = 3


def _resumo(matriz: Matriz, codigo: str) -> dict:
    d = matriz.disciplina(codigo)
    return {"codigo": d.codigo, "nome": d.nome, "periodo": d.periodo, "carga_horaria": d.carga_horaria}


def _carga(matriz: Matriz, codigos) -> int:
    return sum(matriz.disciplina(c).carga_horaria for c in codigos)


def impacto_matricula(matriz: Matriz, aluno: AlunoDemo, codigo: str) -> dict:
    sit = status(matriz, aluno, codigo)
    diretos = matriz.dependentes(codigo)
    todos = matriz.dependentes(codigo, transitivo=True)
    indiretos = [c for c in todos if c not in diretos]

    # O que muda se a disciplina for concluída com sucesso?
    apos = replace(aluno, concluidas=aluno.concluidas | {codigo}, cursando=aluno.cursando - {codigo})
    desbloqueia = [
        c for c in diretos
        if status(matriz, aluno, c).status == Status.BLOQUEADA
        and status(matriz, apos, c).status == Status.DISPONIVEL
    ]

    ativas = aluno.cursando | aluno.selecionadas
    pendentes_dep = [c for c in todos if c not in aluno.concluidas]
    gargalo = len(pendentes_dep) >= LIMITE_GARGALO

    avisos = []
    if sit.status == Status.BLOQUEADA:
        avisos += sit.motivos(matriz)
    if gargalo:
        avisos.append(
            f"{codigo} é pré-requisito, direto ou indireto, de {len(pendentes_dep)} "
            "disciplinas ainda não concluídas."
        )

    return {
        "disciplina": _resumo(matriz, codigo),
        "situacao": {"status": sit.status.value, "motivos": sit.motivos(matriz)},
        "prerequisitos": [
            {**_resumo(matriz, r), "atendido": r in aluno.concluidas} for r in matriz.prerequisitos(codigo)
        ],
        "dependentes_diretos": [_resumo(matriz, c) for c in diretos],
        "dependentes_indiretos": [_resumo(matriz, c) for c in indiretos],
        "desbloqueia": [_resumo(matriz, c) for c in desbloqueia],
        "carga_semestre": {
            "antes": _carga(matriz, ativas),
            "depois": _carga(matriz, ativas | {codigo}),
        },
        "gargalo": gargalo,
        "avisos": avisos,
    }


def impacto_trancamento(matriz: Matriz, aluno: AlunoDemo, codigo: str) -> dict:
    """Compara a projeção 'sem trancar' x 'trancando' ao fim do semestre.

    Premissa explícita da simulação: o aluno conclui as demais disciplinas em
    andamento. Trancar é apresentado como alteração de sequência, não perda.
    """
    if codigo not in aluno.cursando:
        raise ValueError(f"{codigo} não está em andamento; só é possível simular o trancamento de disciplinas em andamento.")

    base = replace(aluno, cursando=frozenset(), selecionadas=frozenset())
    antes = replace(base, concluidas=aluno.concluidas | aluno.cursando)
    depois = replace(base, concluidas=aluno.concluidas | (aluno.cursando - {codigo}))

    todos = [c for c in matriz.dependentes(codigo, transitivo=True) if c not in aluno.concluidas]
    ficam_bloqueadas = []
    for c in todos:
        s_antes, s_depois = status(matriz, antes, c), status(matriz, depois, c)
        if s_antes.status == Status.DISPONIVEL and s_depois.status == Status.BLOQUEADA:
            ficam_bloqueadas.append({**_resumo(matriz, c), "motivos": s_depois.motivos(matriz)})
    diretamente = {x["codigo"] for x in ficam_bloqueadas}
    atraso_potencial = [_resumo(matriz, c) for c in todos if c not in diretamente]

    avisos = ["Trancar não é perda definitiva: a disciplina continua pendente e pode ser cursada em semestre posterior."]
    if ficam_bloqueadas:
        avisos.append(
            f"Na projeção, {len(ficam_bloqueadas)} disciplina(s) deixariam de estar disponíveis no próximo semestre."
        )

    return {
        "simulacao": True,
        "premissa": "Projeção assume conclusão das demais disciplinas em andamento.",
        "disciplina": _resumo(matriz, codigo),
        "carga_semestre": {
            "antes": _carga(matriz, aluno.cursando),
            "depois": _carga(matriz, aluno.cursando - {codigo}),
        },
        "ficam_bloqueadas": ficam_bloqueadas,
        "atraso_potencial": atraso_potencial,
        "avisos": avisos,
    }
