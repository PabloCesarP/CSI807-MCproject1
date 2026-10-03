import pytest

from engine.horarios import Horario, Turma, conflitos


def turma(i, disc, *hs):
    return Turma(i, disc, "A", tuple(Horario.parse(h) for h in hs))


def test_parse_e_str():
    assert str(Horario.parse("SEG 08:00-09:40")) == "SEG 08:00-09:40"


def test_sobreposicao_conflita():
    assert Horario.parse("SEG 08:00-09:40").conflita(Horario.parse("SEG 09:00-10:40"))


def test_horarios_adjacentes_nao_conflitam():
    assert not Horario.parse("SEG 08:00-09:40").conflita(Horario.parse("SEG 09:40-11:20"))


def test_dias_diferentes_nao_conflitam():
    assert not Horario.parse("SEG 08:00-09:40").conflita(Horario.parse("TER 08:00-09:40"))


def test_conflitos_entre_turmas():
    a = turma("1", "CSI101", "SEG 08:00-09:40", "QUA 08:00-09:40")
    b = turma("2", "CSI011", "QUA 09:00-10:40")
    c = turma("3", "CSI807", "SEX 08:00-09:40")
    achados = conflitos([a, b, c])
    assert len(achados) == 1 and {achados[0][0].id, achados[0][1].id} == {"1", "2"}


@pytest.mark.parametrize("txt", ["segunda 8h", "XXX 08:00-09:00", "SEG 10:00-09:00"])
def test_horario_invalido(txt):
    with pytest.raises(ValueError):
        Horario.parse(txt)
