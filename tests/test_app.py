import pytest

from app import create_app


@pytest.fixture()
def client():
    return create_app({"TESTING": True}).test_client()


def test_pagina_inicial(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "dados fictícios" in r.get_data(as_text=True)


def test_css_servido_de_static(client):
    assert client.get("/static/css/style.css").status_code == 200


def test_api_disciplina(client):
    r = client.get("/matriz/api/disciplina/CSI101")
    assert r.status_code == 200
    j = r.get_json()
    assert [d["codigo"] for d in j["dependentes_diretos"]] == ["CSI102", "CSI103", "CSI301"]


def test_api_disciplina_inexistente(client):
    assert client.get("/matriz/api/disciplina/XXX000").status_code == 404
