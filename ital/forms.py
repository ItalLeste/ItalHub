from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TimeField
from wtforms.validators import DataRequired
from datetime import datetime

class FormLogin(FlaskForm):
    usuario = StringField("Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class FormCadastroUsuario(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    # telefone = StringField("Telefone", validators=[DataRequired()])
    # email = StringField("Email", validators=[DataRequired()])
    # cargo = SelectField('Cargo', choices=['Auxiliar Administrativo', 'Ajudante Geral', 'Auxiliar Técnico', 'Inspetor Técnico', 'Responsável Técnico'])
    # data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    # # idade calcular
    # cpf = StringField('CPF', validators=[DataRequired()])
    # rg = StringField('RG', validators=[DataRequired()])
    # rg_emissao = DateField('Emissão RG', validators=[DataRequired()])
    # # rg_validade calcular
    # numero_cnh = StringField('Número CNH', validators=[DataRequired()])
    # categoria_cnh = SelectField('Categoria CNH', choices=['A', 'B', 'C', 'D', 'E', 'AB', 'AC', 'AD', 'AE'])
    # validade_cnh = DateField('Validade CNH', validators=[DataRequired()])
    # formacao = StringField('Formação', validators=[DataRequired()])


    # cep = StringField('CEP', validators=[DataRequired()])
    # endereco = StringField('Endereço', validators=[DataRequired()])
    # numero = StringField('Número', validators=[DataRequired()])
    # complemento = StringField('Complemento')
    # bairro = StringField('Bairro', validators=[DataRequired()])
    # cidade = StringField('Cidade', validators=[DataRequired])
    # uf = StringField('UF', validators=[DataRequired()])

    # data_admissao = DateField('Data de Admissão', validators=[DataRequired()])
    # data_aso = DateField('Data de ASO', validators=[DataRequired()])
    # # validade_aso calcular => data_aso + 1 ano
    # numero_crea_cft = StringField('Número CREA/CFT')
    # validade_crea_cft = DateField('Validade CREA/CFT')
    
    senha = PasswordField("Senha", validators=[DataRequired()])
    

# Forms DTP
class FormDTPCadastrarInspecao(FlaskForm):
    numero_relatorio = StringField('Número do Relatório', validators=[DataRequired()])
    placa = StringField('Placa', validators=[DataRequired()])
    data_aprovacao = DateField('Data da Aprovação', validators=[DataRequired()])
    modalidade = SelectField('Modalidade', choices=['Escolar até 3.5t', 'Escolar maior que 3.5t', 'Taxi'], validators=[DataRequired()], default='Escolar até 3.5t')
    numero_crm_alvara = StringField('Número CRM/Alvara', validators=[DataRequired()], description='Apenas números.')
    validade_crm_alvara = DateField('Validade CRM/Alvara', validators=[DataRequired()])
    condutor = StringField('Condutor', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()], description='Apenas números')
    status_wpp = SelectField('Status WhatsApp', choices=['enviar', 'enviado', 'confirmação', 'renovação'], validators=[DataRequired()], default='Enviar')
    btn_cadastrar = SubmitField('Cadastrar Inspeção')

class FormDTPEditarInspecao(FlaskForm):
    ...


# Forms Relatorios
class FormDataRelatorios(FlaskForm):
    data_inicio = DateField('Data de Início', validators=[DataRequired()])
    data_fim = DateField('Data de Fim', validators=[DataRequired()])
    btn_gerar = SubmitField('Gerar Relatório')


# Forms Área Restrita
# Form Corretor de Ruidos
class FormCorretorRuido(FlaskForm):
    numero_ficha = StringField('Número Ficha', validators=[DataRequired()], default=9701)
    placa = StringField('Placa', validators=[DataRequired()], default='ABC1234')
    limite_ruido = StringField('Limite de Ruido', validators=[DataRequired()], default=95)
    rpm_ensaio = StringField('RPM Ensaio', validators=[DataRequired()], default=4000)
    rpm_ml = StringField('RPM ML', validators=[DataRequired()], default=850)
    resultado = SelectField('Resultado', choices=['APROVADO', 'REPROVADO'], validators=[DataRequired()], default='APROVADO')
    qtd_leituras = SelectField('Quantidade de Leituras', choices=[5, 7, 9], validators=[DataRequired()], default=5)
    temp_motor = StringField('Temperatura do Motor', validators=[DataRequired()], default=90)
    temp_ar = StringField('Temperatura do Ar', validators=[DataRequired()], default=25)
    pressao_atm = StringField('Pressão Atmosferica', validators=[DataRequired()], default=92)
    velocidade_vento = StringField('Velocidade do Vento', validators=[DataRequired()], default=0.01)
    posicao_motor = SelectField('Posição do Motor', choices=['Central','Dianteiro', 'Traseiro'], validators=[DataRequired()], default='Dianteiro')
    posicao_escapamento = SelectField('Posição do Escapamento', choices=['Traseiro, horizontal, unitário','Traseiro, horizontal, duplo', 'Outros'], validators=[DataRequired()], default='Traseiro, horizontal, unitário')
    qtd_escapamentos = StringField('Quantidade de Escapamentos', validators=[DataRequired()], default=1)
    valor_ultimo_ajuste = StringField('Valor do Ultimo Ajuste', validators=[DataRequired()], default=94.2)
    data_ultimo_ajuste = DateField('Data do Ultimo Ajuste', validators=[DataRequired()], default=datetime.now())
    hora_ultimo_ajuste = StringField('Hora do Ultimo Ajuste', validators=[DataRequired()], default=datetime.now().strftime('%H:%M:%S'))
    inicio_teste = StringField('Inicio do Teste', validators=[DataRequired()], default=datetime.now().strftime('%H:%M:%S'))
    fim_teste = StringField('Fim do Teste', validators=[DataRequired()], default=datetime.now().strftime('%H:%M:%S'))
    btn_gerar = SubmitField('Gerar Relatório')