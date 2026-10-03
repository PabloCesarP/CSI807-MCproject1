import pytest

from engine.aluno import AlunoDemo
from engine.impacto import impacto_matricula, impacto_trancamento


def aluno(**kw):
    return AlunoDemo(id="t", nome="Teste", **{k: frozenset(v) for k, v in kw.items()})


def codigos(lista):
    return {x["codigo"] for x in lista}


def test_impacto_matricula_csi101(matriz):
    r = impacto_matricula(matriz, aluno(), "CSI101")
    assert codigos(r["dependentes_diretos"]) == {"CSI102", "CSI103", "CSI301"}
    assert "CSI104" in codigos(r["dependentes_indiretos"])
    # CSI301 também exige CSI211, então concluir só CSI101 não a libera
    assert codigos(r["desbloqueia"]) == {"CSI102", "CSI103"}
    assert r["gargalo"] is True


def test_impacto_matricula_bloqueada_traz_motivo(matriz):
    r = impacto_matricula(matriz, aluno(), "CSI102")
    assert r["situacao"]["status"] == "bloqueada"
    assert any("CSI101" in m for m in r["avisos"])


def test_carga_do_semestre(matriz):
    a = aluno(cursando={"CSI102"}, selecionadas={"CSI011"})
    r = impacto_matricula(matriz, a, "CSI807")
    assert r["carga_semestre"] == {"antes": 120, "depois": 180}


def test_trancamento_mostra_disciplinas_afetadas(matriz):
    a = aluno(concluidas={"CSI101"}, cursando={"CSI102", "CSI103"})
    r = impacto_trancamento(matriz, a, "CSI103")
    assert {"CSI104", "CSI412", "CSI602"} <= codigos(r["ficam_bloqueadas"])
    assert r["carga_semestre"] == {"antes": 120, "depois": 60}
    assert r["simulacao"] is True
    assert any("não é perda definitiva" in m for m in r["avisos"])


def test_trancar_disciplina_sem_dependentes_afetados(matriz):
    a = aluno(cursando={"ENP144"})
    r = impacto_trancamento(matriz, a, "ENP144")
    assert r["ficam_bloqueadas"] == []


def test_so_tranca_disciplina_em_andamento(matriz):
    with pytest.raises(ValueError):
        impacto_trancamento(matriz, aluno(), "CSI101")
