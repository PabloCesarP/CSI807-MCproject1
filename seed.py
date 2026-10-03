from app import app
from models import db, Disciplina, PreRequisito, AlunoDemo, CenarioDemo
import json

def popular_banco():
    with app.app_context():
        # Limpa dados antigos para evitar duplicação em testes
        db.drop_all()
        db.create_all()

        # 1. Inserir Disciplinas do 1º Período
        d1 = Disciplina(codigo='CSI101', nome='Programação de Computadores I', periodo=1, carga_horaria=60, tipo='Obrigatória')
        d2 = Disciplina(codigo='CEA060', nome='Fundamentos de Cálculo', periodo=1, carga_horaria=60, tipo='Obrigatória')
        
        # 2. Inserir Disciplinas do 2º Período
        d3 = Disciplina(codigo='CSI102', nome='Programação de Computadores II', periodo=2, carga_horaria=60, tipo='Obrigatória')
        d4 = Disciplina(codigo='CSI103', nome='Algoritmos e Estruturas de Dados I', periodo=2, carga_horaria=60, tipo='Obrigatória')

        db.session.add_all([d1, d2, d3, d4])
        db.session.commit()

        # 3. Inserir Pré-requisitos (As "setas" da matriz)
        # CSI102 depende de CSI101
        pr1 = PreRequisito(disciplina_codigo='CSI102', requisito_codigo='CSI101')
        # CSI103 depende de CSI101
        pr2 = PreRequisito(disciplina_codigo='CSI103', requisito_codigo='CSI101')
        
        db.session.add_all([pr1, pr2])

        # 4. Inserir Aluno e Cenário de Demonstração
        aluno = AlunoDemo(nome="João Silva (Fictício)", curso="Sistemas de Informação", periodo=2)
        db.session.add(aluno)

        cenario1 = CenarioDemo(
            nome="Cenário 1 — Aluno no início do curso (Ajuste de Matrícula)",
            configuracao=json.dumps({"disciplinas_concluidas": ["CSI101", "CEA060"]})
        )
        db.session.add(cenario1)

        db.session.commit()
        print("✅ Banco de dados populado com sucesso! Matriz e Cenários criados.")

if __name__ == '__main__':
    popular_banco()
