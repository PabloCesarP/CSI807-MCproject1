from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass


class MatrizInvalida(ValueError):
    """Dados da matriz inconsistentes (código desconhecido, ciclo...)."""


class DisciplinaNaoEncontrada(KeyError):
    pass


@dataclass(frozen=True)
class Disciplina:
    codigo: str
    nome: str
    periodo: int
    carga_horaria: int
    tipo: str  # obrigatoria | eletiva | tcc | projeto_integrador
    horas_minimas: int = 0  # pré-requisito por carga horária concluída
    observacao: str | None = None


class Matriz:
    """Grafo de dependências entre disciplinas.

    Aresta requisito -> disciplina ("requisito é pré-requisito de disciplina").
    """

    def __init__(self, disciplinas: list[Disciplina], prerequisitos: list[tuple[str, str]]):
        """prerequisitos: lista de pares (disciplina, requisito)."""
        self._disc = {d.codigo: d for d in disciplinas}
        if len(self._disc) != len(disciplinas):
            raise MatrizInvalida("Há códigos de disciplina duplicados.")
        self._requisitos: dict[str, set[str]] = defaultdict(set)
        self._dependentes: dict[str, set[str]] = defaultdict(set)
        for disciplina, requisito in prerequisitos:
            for c in (disciplina, requisito):
                if c not in self._disc:
                    raise MatrizInvalida(f"Código desconhecido na matriz: {c}")
            self._requisitos[disciplina].add(requisito)
            self._dependentes[requisito].add(disciplina)
        self._checar_ciclos()

    # ---- consulta -------------------------------------------------------
    def disciplina(self, codigo: str) -> Disciplina:
        try:
            return self._disc[codigo]
        except KeyError:
            raise DisciplinaNaoEncontrada(codigo) from None

    def todas(self) -> list[Disciplina]:
        return [self._disc[c] for c in self._ordenar(self._disc)]

    def por_periodo(self) -> dict[int, list[Disciplina]]:
        res: dict[int, list[Disciplina]] = defaultdict(list)
        for d in self.todas():
            res[d.periodo].append(d)
        return dict(res)

    def prerequisitos(self, codigo: str) -> list[str]:
        self.disciplina(codigo)
        return self._ordenar(self._requisitos.get(codigo, ()))

    def dependentes(self, codigo: str, transitivo: bool = False) -> list[str]:
        """Disciplinas que dependem de `codigo` (diretas ou toda a cadeia)."""
        self.disciplina(codigo)
        if not transitivo:
            return self._ordenar(self._dependentes.get(codigo, ()))
        vistos: set[str] = set()
        fila = deque([codigo])
        while fila:
            atual = fila.popleft()
            for d in self._dependentes.get(atual, ()):
                if d not in vistos:
                    vistos.add(d)
                    fila.append(d)
        return self._ordenar(vistos)

    # ---- internos -------------------------------------------------------
    def _ordenar(self, codigos) -> list[str]:
        return sorted(codigos, key=lambda c: (self._disc[c].periodo, c))

    def _checar_ciclos(self) -> None:
        estado: dict[str, int] = {}  # 1 = visitando, 2 = concluído

        def visitar(c: str) -> None:
            estado[c] = 1
            for r in self._requisitos.get(c, ()):
                if estado.get(r) == 1:
                    raise MatrizInvalida(f"Ciclo de pré-requisitos envolvendo {c} e {r}.")
                if r not in estado:
                    visitar(r)
            estado[c] = 2

        for c in self._disc:
            if c not in estado:
                visitar(c)
