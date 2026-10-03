# CSI807-MCproject1 – Apoio à Vida Acadêmica (Grupo 3: Matriz Curricular)

Protótipo acadêmico **independente** (sem integração com o Minha UFOP, apenas dados fictícios) que mostra
o impacto de escolhas de matrícula e trancamento na matriz curricular de Sistemas de Informação – UFOP/João Monlevade.

## Como rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug      # http://127.0.0.1:5000
python -m pytest                 # testes do motor e do app
```

> Se for gerar o `requirements.txt` de novo no Windows: `pip freeze > requirements.txt` no **PowerShell** grava em
> UTF-16 e quebra o `pip install`. Use o CMD, ou `pip freeze | Out-File -Encoding utf8 requirements.txt`.

## Estrutura

- `engine/` – regras de negócio (Python puro, sem Flask): grafo da matriz, status, horários, impacto.
- `data/` – matriz em JSON (`disciplinas.json`, `prerequisitos.json`) e, futuramente, turmas e cenários.
- `blueprints/` – um módulo Flask por funcionalidade (matriz, matrícula, trancamento, demo).
- `templates/`, `static/` – interface.
- `tests/` – testes automatizados.
- `docs/` – respostas do Trabalho 1 (roteiro e tabela de requisitos da informação).

## Status das fases

- [x] Fase 0 – higiene do repositório
- [x] Fase 1 – dados da matriz e motor (status, dependentes, conflito de horário, impacto)
- [ ] Fase 2 – layout base e CSS
- [ ] Fase 3 – modo demonstração e cenários
- [ ] Fase 4 – matriz curricular interativa
- [ ] Fase 5 – ajuste de matrícula e grade semanal
- [ ] Fase 6 – painel de impacto
- [ ] Fase 7 – trancamento
- [ ] Fase 8 – refino e publicação

## Pendências nos dados da matriz (conferir na fonte oficial)

Os campos `observacao` em `data/disciplinas.json` marcam o que foi cadastrado provisoriamente:

1. **CSI997 (TCC II)**: a imagem indica pré-requisito `CSI996`, que não existe na tabela. Provisório: `CSI992` (TCC I).
2. **CSI992 (TCC I)**: "CSI902 / 1.800h" foi cadastrado como CSI902 **e** 1.800h. Confirmar se é "e" ou "ou".
3. **CSI990 (Projeto Integrador I)**: pré-requisito "Projeto/integração" é vago. Provisório: nenhum.
4. **Eletivas I–V**: sem código na matriz; usados códigos internos `ELE-1` a `ELE-5`.
5. O adendo cita só CSI102 e CSI103 como dependentes de CSI101, mas **CSI301** (Redes I) também exige CSI101 + CSI211.
