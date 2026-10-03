from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .aluno import AlunoDemo
from .matriz import Matriz


class Status(str, Enum):
    CONCLUIDA = "concluida"
    CURSANDO = "cursando"
    DISPONIVEL = "disponivel"  # pré-requisitos atendidos
    BLOQUEADA = "bloqueada"  # falta pré-requisito


@dataclass(frozen=True)
class Situacao:
    status: Status
    requisitos_faltantes: tuple[str, ...] = ()
    horas_faltantes: int = 0

    def motivos(self, matriz: Matriz) -> list[str]:
        """Mensagens claras explicando o bloqueio (regra de negócio nº 9)."""
        msgs = []
        for c in self.requisitos_faltantes:
            msgs.append(f"Falta concluir {c} – {matriz.disciplina(c).nome}.")
        if self.horas_faltantes:
            msgs.append(f"Faltam {self.horas_faltantes}h de carga horária concluída.")
        return msgs


def horas_concluidas(matriz: Matriz, aluno: AlunoDemo) -> int:
    return sum(matriz.disciplina(c).carga_horaria for c in aluno.concluidas)


def status(matriz: Matriz, aluno: AlunoDemo, codigo: str) -> Situacao:
    """Status de uma disciplina para o aluno.

    Só disciplinas CONCLUÍDAS satisfazem pré-requisito (cursando não conta).
    "Pendente" = qualquer disciplina que não está concluída; ver `pendentes()`.
    """
    disc = matriz.disciplina(codigo)
    if codigo in aluno.concluidas:
        return Situacao(Status.CONCLUIDA)
    if codigo in aluno.cursando:
        return Situacao(Status.CURSANDO)
    faltam = tuple(r for r in matriz.prerequisitos(codigo) if r not in aluno.concluidas)
    horas_falta = max(0, disc.horas_minimas - horas_concluidas(matriz, aluno))
    if faltam or horas_falta:
        return Situacao(Status.BLOQUEADA, faltam, horas_falta)
    return Situacao(Status.DISPONIVEL)


def pendentes(matriz: Matriz, aluno: AlunoDemo) -> list[str]:
    return [d.codigo for d in matriz.todas() if d.codigo not in aluno.concluidas]
