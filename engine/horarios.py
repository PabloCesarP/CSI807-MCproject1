from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import combinations

DIAS = ("SEG", "TER", "QUA", "QUI", "SEX", "SAB")
_PADRAO = re.compile(r"^(\w{3}) (\d{2}):(\d{2})-(\d{2}):(\d{2})$")


@dataclass(frozen=True)
class Horario:
    dia: str
    inicio: int  # minutos desde 00:00
    fim: int

    def __post_init__(self):
        if self.dia not in DIAS:
            raise ValueError(f"Dia inválido: {self.dia}")
        if self.inicio >= self.fim:
            raise ValueError("O início deve ser anterior ao fim.")

    @classmethod
    def parse(cls, texto: str) -> "Horario":
        """Ex.: 'SEG 08:00-09:40'."""
        m = _PADRAO.match(texto.strip())
        if not m:
            raise ValueError(f"Formato de horário inválido: {texto!r}")
        dia, h1, m1, h2, m2 = m.groups()
        return cls(dia, int(h1) * 60 + int(m1), int(h2) * 60 + int(m2))

    def conflita(self, outro: "Horario") -> bool:
        # horários que apenas se tocam (fim == início) não conflitam
        return self.dia == outro.dia and self.inicio < outro.fim and outro.inicio < self.fim

    def __str__(self) -> str:
        f = lambda t: f"{t // 60:02d}:{t % 60:02d}"
        return f"{self.dia} {f(self.inicio)}-{f(self.fim)}"


@dataclass(frozen=True)
class Turma:
    id: str
    disciplina: str
    codigo_turma: str
    horarios: tuple[Horario, ...]
    vagas: int = 0


def conflitos(turmas: list[Turma]) -> list[tuple[Turma, Turma, Horario, Horario]]:
    """Pares de turmas com sobreposição, com os horários que colidem."""
    achados = []
    for a, b in combinations(turmas, 2):
        for ha in a.horarios:
            for hb in b.horarios:
                if ha.conflita(hb):
                    achados.append((a, b, ha, hb))
    return achados
