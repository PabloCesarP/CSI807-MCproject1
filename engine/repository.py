"""Camada de acesso a dados. Hoje lê JSON; amanhã pode ler SQLite sem mudar o motor."""
from __future__ import annotations

import json
from pathlib import Path

from .matriz import Disciplina, Matriz


class JsonRepository:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)

    def _ler(self, nome: str):
        with open(self.data_dir / nome, encoding="utf-8") as f:
            return json.load(f)

    def carregar_matriz(self) -> Matriz:
        disciplinas = [Disciplina(**d) for d in self._ler("disciplinas.json")]
        prereqs = [(p["disciplina"], p["requisito"]) for p in self._ler("prerequisitos.json")]
        return Matriz(disciplinas, prereqs)
