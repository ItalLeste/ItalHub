from ital import app, engine
from ital.models import QuadroFuncionarios, DTP_Credenciais, DTP_Relatorios, DTP_Condutores, DTP_Inspecoes, DTP_Precos, DTP_Stats


if __name__ == "__main__":
    with app.app_context():  # Cria o banco de dados. Se necessário.
        engine.drop_all()
        engine.create_all()

        # Cria o admin
        nome_completo = 'admin'
        senha = 'admin'
        nivel_acesso = 'admin'
        apelido = 'admin'

        # Verifica se o usuário já existe
        usuario_existe = QuadroFuncionarios.query.filter_by(nome_completo=nome_completo).first()

        if not usuario_existe:
            novo_usuario = QuadroFuncionarios(nome_completo=nome_completo, senha=senha, nivel_acesso=nivel_acesso, apelido=apelido)
            engine.session.add(novo_usuario)
            engine.session.commit()

        # Adiciona preços
        from datetime import datetime
        escolar1 = 226.00
        escolar2 = 307.00
        taxi = escolar1
        ano = datetime.now().year
        
        novo_preco = DTP_Precos(ano=ano, escolar1_valor=escolar1, escolar2_valor=escolar2, taxi_valor=taxi)
        engine.session.add(novo_preco)
        engine.session.commit()

        # Cria os registros iniciais de stats
        anos = [2022, 2023, 2024]
        meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        for ano in anos:
            for mes in meses:
                novo_registro = DTP_Stats(ano=ano, mes=mes, modalidade='escolar', inspecoes_aprovadas=0, inspecoes_reprovadas=0, inspecoes_total=0)
                engine.session.add(novo_registro)
                engine.session.commit()

                novo_registro = DTP_Stats(ano=ano, mes=mes, modalidade='taxi', inspecoes_aprovadas=0, inspecoes_reprovadas=0, inspecoes_total=0)
                engine.session.add(novo_registro)
                engine.session.commit()

        from ital.modules.controle_dtp.gerenciador_dtp import GerenciadorDTP
        g = GerenciadorDTP()
        # # g.cadastrar_relatorio(1)

        # Cadastrar inspeção.
        g.cadastrar_inspecao(numero_relatorio=1, placa='ABC1234', modalidade='escolar1', data_aprovacao=datetime.now(), numero_crm_alvara=123456, validade_crm_alvara=datetime.now(), nome_condutor='NomedoCondutor', telefone_condutor='11999999999', status_whatsapp=1)

        # Cadastrar stats
        g.cadastrar_stats_dtp(ano=2025, mes=1, modalidade='escolar', total_aprovadas=1, total_reprovadas=1, total_geral=2)


    app.run(host='0.0.0.0', debug=True, use_reloader=True)  # Inicia o servidor.