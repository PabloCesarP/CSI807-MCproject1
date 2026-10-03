from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Cadastro da Matriz
class Disciplina(db.Model):
    __tablename__ = 'disciplina'
    codigo = db.Column(db.String(10), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    periodo = db.Column(db.Integer, nullable=False) # 1 a 8
    carga_horaria = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50)) # Obrigatória, Eletiva, etc.

# Relaciona dependências (Pré-requisitos)
class PreRequisito(db.Model):
    __tablename__ = 'pre_requisito'
    id = db.Column(db.Integer, primary_key=True)
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo'), nullable=False)
    requisito_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo'), nullable=False)

# Oferta usada no ajuste
class Turma(db.Model):
    __tablename__ = 'turma'
    id = db.Column(db.Integer, primary_key=True)
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo'), nullable=False)
    codigo_turma = db.Column(db.String(20), nullable=False)
    horarios = db.Column(db.String(100)) # Ex: "Seg 17:10, Ter 19:00"
    vagas = db.Column(db.Integer)

# 2. Perfil Fictício usado na apresentação
class AlunoDemo(db.Model):
    __tablename__ = 'aluno_demo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), default="Sistemas de Informação")
    periodo = db.Column(db.Integer, default=1)
    semestre = db.Column(db.String(20), default="2026.1")

# Guarda concluída/cursando/pendente
class SituacaoAluno(db.Model):
    __tablename__ = 'situacao_aluno'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno_demo.id'), nullable=False)
    disciplina_codigo = db.Column(db.String(10), db.ForeignKey('disciplina.codigo'), nullable=False)
    status = db.Column(db.String(20)) # 'Concluída', 'Cursando', 'Pendente'

# Permite carregar cenários prontos para apresentação
class CenarioDemo(db.Model):
    __tablename__ = 'cenario_demo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    configuracao = db.Column(db.Text) # JSON com o estado do cenário
