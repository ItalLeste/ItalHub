from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

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