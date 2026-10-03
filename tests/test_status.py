from engine.aluno import AlunoDemo
from engine.status import Status, horas_concluidas, status


def aluno(**kw):
    return AlunoDemo(id="t", nome="Teste", **{k: frozenset(v) for k, v in kw.items()})


def test_sem_prerequisito_esta_disponivel(matriz):
    assert status(matriz, aluno(), "CSI101").status == Status.DISPONIVEL


def test_bloqueada_explica_o_motivo(matriz):
    sit = status(matriz, aluno(), "CSI102")
    assert sit.status == Status.BLOQUEADA
    assert sit.requisitos_faltantes == ("CSI101",)
    assert "CSI101" in sit.motivos(matriz)[0]


def test_concluir_requisito_libera(matriz):
    assert status(matriz, aluno(concluidas={"CSI101"}), "CSI102").status == Status.DISPONIVEL


def test_cursando_requisito_nao_libera(matriz):
    assert status(matriz, aluno(cursando={"CSI101"}), "CSI102").status == Status.BLOQUEADA


def test_concluida_e_cursando(matriz):
    a = aluno(concluidas={"CSI101"}, cursando={"CSI102"})
    assert status(matriz, a, "CSI101").status == Status.CONCLUIDA
    assert status(matriz, a, "CSI102").status == Status.CURSANDO


def test_pre_requisito_por_horas(matriz):
    sit = status(matriz, aluno(), "ENP493")
    assert sit.status == Status.BLOQUEADA and sit.horas_faltantes == 1800
    ate_p6 = {d.codigo for p in range(1, 7) for d in matriz.por_periodo()[p]}
    a = aluno(concluidas=ate_p6)
    assert horas_concluidas(matriz, a) >= 1800
    assert status(matriz, a, "ENP493").status == Status.DISPONIVEL
