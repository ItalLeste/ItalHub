from ital import app, engine
from datetime import datetime
from flask_login import UserMixin

# RH
class QuadroFuncionarios(engine.Model, UserMixin):
    __tablename__ = 'quadro_funcionarios'
    
    # Dados pessoais
    id = engine.Column(engine.Integer, primary_key=True)
    nome_completo = engine.Column(engine.String(100), nullable=False)
    # telefone = engine.Column(engine.String(20), nullable=False)
    # email = engine.Column(engine.String(100), nullable=True)
    # cargo = engine.Column(engine.Enum('Auxiliar Administrativo', 'Responsável Técnico', 'Inspetor Técnico', 'Ajudante Geral', 'admin', name='setor_enum'), nullable=False)
    # data_nascimento = engine.Column(engine.Date, nullable=False)
    # idade = engine.Column(engine.Integer, nullable=False)
    # cpf = engine.Column(engine.String(11), nullable=False)
    # rg = engine.Column(engine.String(20), nullable=False)
    # rg_emissao = engine.Column(engine.Date, nullable=False)
    # rg_validade = engine.Column(engine.Date, nullable=False)
    # numero_cnh = engine.Column(engine.String(20), nullable=True)
    # categoria_cnh = engine.Column(engine.String(5), nullable=True)
    # validade_cnh = engine.Column(engine.Date, nullable=True)
    # formacao = engine.Column(engine.String(100), nullable=False)
    # senha = engine.Column(engine.String(10), nullable=False)

    # # Endereço
    # cep = engine.Column(engine.String(8), nullable=False)
    # endereco = engine.Column(engine.String(100), nullable=False)
    # numero = engine.Column(engine.String(10), nullable=False)
    # complemento = engine.Column(engine.String(20), nullable=True)
    # bairro = engine.Column(engine.String(50), nullable=False)
    # cidade = engine.Column(engine.String(50), nullable=False)
    # uf = engine.Column(engine.String(2), nullable=False)

    # # Admissão
    # data_admissao = engine.Column(engine.Date, nullable=False)
    # data_aso = engine.Column(engine.Date, nullable=False)
    # aso_validade = engine.Column(engine.Date, nullable=False)
    # numero_crea_cft = engine.Column(engine.String(20), nullable=True)
    # crea_cft_validade = engine.Column(engine.Date, nullable=True)

    apelido = engine.Column(engine.String(20), nullable=False)
    senha = engine.Column(engine.String(10), nullable=False)
    nivel_acesso = engine.Column(engine.Enum('admin', 'diretoria', 'técnico', 'administrativo', name='nivel_acesso_enum'), nullable=False, default='administrativo')

# DTP
class DTP_Credenciais(engine.Model):
    __tablename__ = 'dtp_credenciais'

    id = engine.Column(engine.Integer, primary_key=True)
    numero_empresa = engine.Column(engine.String(10), nullable=False)
    login = engine.Column(engine.String(20), nullable=False)
    senha = engine.Column(engine.String(64), nullable=False)

class DTP_Relatorios(engine.Model):
    __tablename__ = 'dtp_relatorios'

    id = engine.Column(engine.Integer, primary_key=True)
    numero_relatorio = engine.Column(engine.Integer, unique=True, nullable=False)
    status_relatorio = engine.Column(engine.Integer, nullable=False) # 0 - Rasurado, 1 - Utilizado
    data_cadastro = engine.Column(engine.Date, nullable=False, default=datetime.utcnow)

class DTP_Condutores(engine.Model):
    __tablename__ = 'dtp_condutores'

    id = engine.Column(engine.Integer, primary_key=True)
    nome = engine.Column(engine.String(100), nullable=False)
    telefone = engine.Column(engine.String(20), nullable=False)
    status_whatsapp = engine.Column(engine.Integer, nullable=False) # 1 - Enviar mensagem, 2 - Mensagem enviada, 3 - Confirmação de emissão do CRM/Alvará, 4 -Renovação CRM/Alvará

class DTP_Inspecoes(engine.Model):
    __tablename__ = 'dtp_inspecoes'

    id = engine.Column(engine.Integer, primary_key=True)
    placa = engine.Column(engine.String(10), nullable=False)
    numero_relatorio = engine.Column(engine.Integer, engine.ForeignKey('dtp_relatorios.numero_relatorio'), nullable=False)
    condutor_id = engine.Column(engine.Integer, engine.ForeignKey('dtp_condutores.id'), nullable=False)
    modalidade = engine.Column(engine.Enum('escolar1', 'escolar2', 'taxi', name='modalidade_enum'), nullable=False)
    valor = engine.Column(engine.DECIMAL, nullable=False)
    data_aprovacao = engine.Column(engine.Date, nullable=False)
    numero_crm_alvara = engine.Column(engine.String(10), nullable=False)
    validade_crm_alvara = engine.Column(engine.Date, nullable=False)

class DTP_Precos(engine.Model):
    __tablename__ = 'dtp_precos'

    id = engine.Column(engine.Integer, primary_key=True)
    ano = engine.Column(engine.Integer, nullable=False, unique=True)
    escolar1_valor = engine.Column(engine.DECIMAL(10, 2), nullable=False)
    escolar2_valor = engine.Column(engine.DECIMAL(10, 2), nullable=False)
    taxi_valor = engine.Column(engine.DECIMAL(10, 2), nullable=False)

class DTP_Stats(engine.Model):
    __tablename__ = 'dtp_stats'

    id = engine.Column(engine.Integer, primary_key=True)
    ano = engine.Column(engine.Integer, nullable=False)
    mes = engine.Column(engine.Integer, nullable=False)
    modalidade = engine.Column(engine.Enum('escolar', 'taxi', name='modalidade_enum'), nullable=False)
    inspecoes_aprovadas = engine.Column(engine.Integer, nullable=False)
    inspecoes_reprovadas = engine.Column(engine.Integer, nullable=False)
    inspecoes_total = engine.Column(engine.Integer, nullable=False)