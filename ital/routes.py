from ital import app, engine
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from ital.forms import FormLogin, FormDTPCadastrarInspecao, FormCadastroUsuario, FormDataRelatorios
from ital.models import QuadroFuncionarios, DTP_Stats
from ital.modules.relatorios.estatisticas_inspecoes import exportar_dados
from ital.modules.controle_dtp.gerenciador_dtp import GerenciadorDTP
from datetime import datetime, date
from dateutil import relativedelta

# Login
@app.route("/", methods=["GET", "POST"])
def index():
    form_login = FormLogin()
    erro_login = False
    if form_login.validate_on_submit():
        usuario_form = form_login.usuario.data.lower()
        senha_form = form_login.senha.data
        usuario = QuadroFuncionarios.query.filter_by(apelido=usuario_form).first()

        if usuario and usuario.senha == senha_form:
            login_user(usuario, remember=True)
            return redirect(url_for('home'))
        else:
            erro_login = True

    return render_template("index.html", form_login=form_login, erro_login=erro_login)

# Tela inicial
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    apelido = current_user.apelido

    return render_template('home.html', apelido=apelido)

@app.route('/cadastrar-usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    form_cadastrar_usuario = FormCadastroUsuario()
    if form_cadastrar_usuario.validate_on_submit():
        nome = form_cadastrar_usuario.nome.data
        senha = form_cadastrar_usuario.senha.data
        novo_usuario = QuadroFuncionarios(nome=nome, senha=senha)
        engine.session.add(novo_usuario)
        engine.session.commit()

        print('Usuário cadastrado com sucesso!')
        
        return redirect(url_for('home'))
    return render_template('cadastrar_usuario.html', form=form_cadastrar_usuario)


@app.route('/controle_dtp/controle-dtp', methods=['GET', 'POST'])
@login_required
def controle_dtp():
    # Pega os anos e meses únicos do banco
    anos_cadastrados = [ano[0] for ano in engine.session.query(DTP_Stats.ano).distinct().all()]
    meses_cadastrados = [mes[0] for mes in engine.session.query(DTP_Stats.mes).distinct().all()]
    ano_selecionado = None
    mes_selecionado = None

    if request.method == 'POST':
        ano_selecionado = request.form.get('ano')
        mes_selecionado = request.form.get('mes')
        print("Ano:", ano_selecionado)
        print("Mês:", mes_selecionado)

        if ano_selecionado and mes_selecionado:
            pass
        
    return render_template('/controle_dtp/controle_dtp.html', anos_cadastrados=anos_cadastrados, meses_cadastrados=meses_cadastrados)

# Ferramentas
@app.route('/ferramentas/ferramentas.html', methods=['GET', 'POST'])
def ferramentas():
    return render_template('/ferramentas/ferramentas.html')

# Relatórios
@app.route('/relatorios/relatorios')
@login_required
def relatorios():
    return render_template('/relatorios/relatorios.html')

@app.route('/relatorios/quantidade-inspecoes', methods=['GET', 'POST'])
@login_required
def controle_estatistico():
    form = FormDataRelatorios()
    dados_escopo = {}
    dados_tipo_veiculo = {}

    if form.validate_on_submit():
        data_inicio = form.data_inicio.data.strftime('%Y-%m-%d')
        data_fim = form.data_fim.data.strftime('%Y-%m-%d')
        inspecoes_escopo, inspecoes_tipo_veiculo = exportar_dados(data_inicio, data_fim)
        aprovado_sinistro = 0
        reprovado_sinistro = 0
        total_sinistro = 0
        aprovado_gnv = 0
        reprovado_gnv = 0
        total_gnv = 0   
        aprovado_modificado = 0
        reprovado_modificado = 0
        total_modificado = 0
        total_geral = 0

        
        for k, v in inspecoes_escopo.items():
            for k2, v2 in v.items():
                periodo = str(k2) + '/' + str(k)
                dados_escopo[periodo] = [v2['SINISTRO'][0], v2['SINISTRO'][1], v2['SINISTRO'][2], v2['GNV'][0], v2['GNV'][1], v2['GNV'][2], v2['MODIFICADO'][0], v2['MODIFICADO'][1], v2['MODIFICADO'][2]]

                aprovado_sinistro += v2['SINISTRO'][0]
                reprovado_sinistro += v2['SINISTRO'][1]
                total_sinistro += v2['SINISTRO'][2]

                aprovado_gnv += v2['GNV'][0]
                reprovado_gnv += v2['GNV'][1]
                total_gnv += v2['GNV'][2]

                aprovado_modificado += v2['MODIFICADO'][0]  
                reprovado_modificado += v2['MODIFICADO'][1]
                total_modificado += v2['MODIFICADO'][2]

                total_geral += v2['SINISTRO'][2] + v2['GNV'][2] + v2['MODIFICADO'][2]   

        for k, v in inspecoes_tipo_veiculo.items():
            dados_tipo_veiculo[k] = v 

        return render_template(
            '/relatorios/quantidade_inspecoes.html', 
            form=form, 
            dados_escopo=dados_escopo, 
            dados_tipo_veiculo=dados_tipo_veiculo, 
            aprovado_sinistro=aprovado_sinistro, 
            reprovado_sinistro=reprovado_sinistro, 
            total_sinistro=total_sinistro, 
            aprovado_gnv=aprovado_gnv, 
            reprovado_gnv=reprovado_gnv, 
            aprovado_modificado=aprovado_modificado, 
            reprovado_modificado=reprovado_modificado, 
            total_gnv=total_gnv, 
            total_modificado=total_modificado, 
            total_geral=total_geral)
    
    return render_template('/relatorios/quantidade_inspecoes.html', form=form, dados_escopo=dados_escopo, dados_tipo_veiculo=dados_tipo_veiculo)

@app.route('/relatorios/relatorio-financeiro')
@login_required
def relatorio_financeiro():
    form = FormDataRelatorios()
    return render_template('/relatorios/relatorio_financeiro.html', form=form)

# Área Restrita
@app.route('/area-restrita/area-restrita')
@login_required
def area_restrita():
    return render_template('/area_restrita/area_restrita.html')

@app.route('/ri-ocultos')
@login_required
def ri_ocultos():
    return render_template('ri_ocultos.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

