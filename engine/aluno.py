from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AlunoDemo:
    """Perfil FICTÍCIO usado no modo demonstração."""

    id: str
    nome: str
    curso: str = "SI"
    periodo: int = 1
    semestre: str = "2026/2"
    concluidas: frozenset[str] = field(default_factory=frozenset)
    cursando: frozenset[str] = field(default_factory=frozenset)
    selecionadas: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def from_dict(cls, d: dict) -> "AlunoDemo":
        return cls(
            id=d["id"],
            nome=d["nome"],
            curso=d.get("curso", "SI"),
            periodo=d.get("periodo", 1),
            semestre=d.get("semestre", "2026/2"),
            concluidas=frozenset(d.get("concluidas", ())),
            cursando=frozenset(d.get("cursando", ())),
            selecionadas=frozenset(d.get("selecionadas", ())),
        )
