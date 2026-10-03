import pytest

from engine.matriz import Disciplina, DisciplinaNaoEncontrada, Matriz, MatrizInvalida


def test_matriz_carrega_44_disciplinas_em_8_periodos(matriz):
    assert len(matriz.todas()) == 44
    assert sorted(matriz.por_periodo()) == list(range(1, 9))


def test_dependentes_diretos_de_csi101(matriz):
    assert matriz.dependentes("CSI101") == ["CSI102", "CSI103", "CSI301"]


def test_dependentes_transitivos_seguem_a_cadeia(matriz):
    cadeia = matriz.dependentes("CSI101", transitivo=True)
    assert "CSI104" in cadeia and "CSI410" in cadeia and "CSI302" in cadeia
    assert "CSI101" not in cadeia


def test_tcc_ii_depende_de_tcc_i_e_metodologia(matriz):
    assert "CSI997" in matriz.dependentes("CSI902", transitivo=True)


def test_prerequisitos_multiplos(matriz):
    assert matriz.prerequisitos("CSI104") == ["CSI102", "CSI103"]


def test_disciplina_inexistente(matriz):
    with pytest.raises(DisciplinaNaoEncontrada):
        matriz.disciplina("XXX000")


def _d(c, p=1):
    return Disciplina(c, c, p, 60, "obrigatoria")


def test_detecta_ciclo():
    with pytest.raises(MatrizInvalida):
        Matriz([_d("A"), _d("B")], [("A", "B"), ("B", "A")])


def test_detecta_codigo_desconhecido():
    with pytest.raises(MatrizInvalida):
        Matriz([_d("A")], [("A", "Z")])
