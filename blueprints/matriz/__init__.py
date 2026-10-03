from flask import Blueprint, current_app, jsonify

from engine.matriz import DisciplinaNaoEncontrada

bp = Blueprint("matriz", __name__, url_prefix="/matriz")


def _resumo(m, codigo):
    d = m.disciplina(codigo)
    return {"codigo": d.codigo, "nome": d.nome, "periodo": d.periodo, "carga_horaria": d.carga_horaria}


@bp.get("/api/disciplina/<codigo>")
def api_disciplina(codigo):
    """Detalhes + pré-requisitos + dependentes (base do clique na matriz)."""
    m = current_app.extensions["matriz"]
    try:
        d = m.disciplina(codigo)
    except DisciplinaNaoEncontrada:
        return jsonify(erro=f"Disciplina {codigo} não encontrada na matriz."), 404
    diretos = m.dependentes(codigo)
    return jsonify(
        disciplina={**_resumo(m, codigo), "tipo": d.tipo, "horas_minimas": d.horas_minimas, "observacao": d.observacao},
        prerequisitos=[_resumo(m, c) for c in m.prerequisitos(codigo)],
        dependentes_diretos=[_resumo(m, c) for c in diretos],
        dependentes_indiretos=[_resumo(m, c) for c in m.dependentes(codigo, transitivo=True) if c not in diretos],
    )
