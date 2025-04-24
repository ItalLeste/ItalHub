from ital import app, engine
from ital.models import DTP_Relatorios, DTP_Condutores, DTP_Inspecoes, DTP_Precos, DTP_Stats
from datetime import datetime
from ital.tools.validadores import validar_placa, validar_telefone, validar_numero_relatorio, validar_nome_completo

class GerenciadorDTP():
    # CREATE
    def cadastrar_relatorio(self, numero_relatorio: int, status_relatorio: int = 1):
        try:
            numero_relatorio = validar_numero_relatorio(numero_relatorio)
            relatorio_cadastrado = engine.session.query(DTP_Relatorios).filter(DTP_Relatorios.numero_relatorio == numero_relatorio).first()

            if not relatorio_cadastrado:
                novo_relatorio = DTP_Relatorios(numero_relatorio=numero_relatorio, status_relatorio=status_relatorio)
                engine.session.add(novo_relatorio)
                engine.session.commit()
                return numero_relatorio, status_relatorio
            else:
                print("Relatório já cadastrado!")
                return False

        except Exception as e:
            print(f"Erro ao cadastrar o relatório: {e}")
            engine.session.rollback()  # Caso ocorra um erro, fazemos o rollback da transação
            return False
    
    def cadastrar_condutor(self, nome_condutor:str, telefone:str, status_whatsapp:int=1):
        nome_condutor = validar_nome_completo(nome_condutor)
        nome_condutor = nome_condutor.title()
        telefone = validar_telefone(telefone)
        condutor_cadastrado = engine.session.query(DTP_Condutores).filter(DTP_Condutores.telefone == telefone).first()

        try:
            if not condutor_cadastrado:
                novo_condutor = DTP_Condutores(nome=nome_condutor, telefone=telefone, status_whatsapp=status_whatsapp)
                engine.session.add(novo_condutor)
                engine.session.commit()
                condutor_id = engine.session.query(DTP_Condutores).filter(DTP_Condutores.nome == nome_condutor).first().id
                return condutor_id, nome_condutor, telefone, status_whatsapp
            else:
                print("Condutor ja cadastrado!")
                return False

        except Exception as e:
            print(f"Erro ao cadastrar o condutor: {e}")
            engine.session.rollback()
            return False
        
    def cadastrar_precos(self, ano:int, escolar1:float, escolar2:float):
        try:
            taxi = escolar1
            preco_existente = DTP_Precos.query.filter_by(ano=ano).first()
            if not preco_existente:
                novo_preco = DTP_Precos(ano=ano, escolar1_valor=escolar1, escolar2_valor=escolar2, taxi_valor=taxi)
                engine.session.add(novo_preco)
                engine.session.commit()
                print(f"Preços do ano {ano} cadastrados com sucesso!")
                return True
            else:
                print(f"Preços do ano {ano} ja cadastrados!")
                return False
        except Exception as e:
            print(f"Erro ao cadastrar ou atualizar os preços: {e}")
            engine.session.rollback()
            return False

    def cadastrar_inspecao(self, numero_relatorio:int, placa:str, modalidade:str, data_aprovacao:datetime, numero_crm_alvara:int, validade_crm_alvara:datetime, nome_condutor:str, telefone_condutor:str, status_whatsapp:int=1):
        def consultar_preco_inspecao(modalidade):
            try:
                precos_modalidade = DTP_Precos.query.filter_by(ano=datetime.now().year).first()
                if modalidade == 'escolar1':
                    return precos_modalidade.escolar1_valor
                elif modalidade == 'escolar2':
                    return precos_modalidade.escolar2_valor
                elif modalidade == 'taxi':
                    return precos_modalidade.taxi_valor
            except Exception as e:
                print(f"Erro ao consultar preços: {e}")
                engine.session.rollback()
                return False
            
        placa = validar_placa(placa)
        numero_relatorio, _ = self.cadastrar_relatorio(numero_relatorio)
        condutor_id, nome_condutor, _, _ = self.cadastrar_condutor(nome_condutor, telefone_condutor, status_whatsapp) 
        modalidade = modalidade.lower()
        valor = consultar_preco_inspecao(modalidade)

        try:
            inspecao_existente = DTP_Inspecoes.query.filter_by(numero_relatorio=numero_relatorio).first()
            if not inspecao_existente:
                nova_inspecao = DTP_Inspecoes(
                    placa = placa,
                    numero_relatorio=numero_relatorio,
                    condutor_id = condutor_id,
                    modalidade = modalidade,
                    valor = valor,
                    data_aprovacao = data_aprovacao,
                    numero_crm_alvara=numero_crm_alvara,
                    validade_crm_alvara=validade_crm_alvara,
                )
                engine.session.add(nova_inspecao)
                engine.session.commit()
                print(f'Inspecão cadastrada com sucesso!')
                return True
            else:
                print(f"Inspeção {numero_relatorio} ja cadastrada!")
                return False
        except Exception as e:
            print(f"Erro ao cadastrar inspecao: {e}")
            engine.session.rollback()
            return False

    def cadastrar_stats_dtp(self, ano:int, mes:int, modalidade:str, total_aprovadas:int, total_reprovadas:int, total_geral:int):
        try:
            stats_existente = DTP_Stats.query.filter_by(ano=ano, mes=mes, modalidade=modalidade).first()
            if not stats_existente:
                novo_registro = DTP_Stats(ano=ano, mes=mes, modalidade=modalidade, inspecoes_aprovadas=total_aprovadas, inspecoes_reprovadas=total_reprovadas, inspecoes_total=total_geral)
                engine.session.add(novo_registro)
                engine.session.commit()
                print(f"Stats DTP  {modalidade} referentes a {mes}/{ano} cadastradas com sucesso!")
                return

        except Exception as e:
            print(f"Erro ao cadastrar stats: {e}")
            engine.session.rollback()
            return

#     # CRUD - Read
#     def consultar_relatorios_nao_cadastrados(self) -> list[int]:
#         """
#         Consulta os números de relatórios ausentes entre o menor e o maior da tabela dtp_relatorios.
#         Retorna uma lista com os números dos relatórios não cadastrados.
#         """
#         try:
#             with Session(bind=self.engine) as session:
#                 # Consultar o menor e o maior número de relatórios
#                 menor_relatorio = session.query(func.min(DTP_Relatorios.numero_relatorio)).scalar()
#                 maior_relatorio = session.query(func.max(DTP_Relatorios.numero_relatorio)).scalar()

#                 if menor_relatorio is None or maior_relatorio is None:
#                     print("Nenhum relatório cadastrado na tabela dtp_relatorios.")
#                     return []

#             relatorios_cadastrados = session.query(DTP_Relatorios.numero_relatorio).all()  # Obter os números de todos os relatórios cadastrados
#             relatorios_cadastrados_set = {r[0] for r in relatorios_cadastrados}  # Conjunto para busca eficiente
#             todos_numeros = set(range(menor_relatorio, maior_relatorio + 1)) # Criar a lista de todos os números no intervalo
#             relatorios_nao_cadastrados = list(todos_numeros - relatorios_cadastrados_set) # Determinar os números de relatórios ausentes
#             relatorios_nao_cadastrados.sort() # Ordenar os números ausentes para retornar de forma organizada
#             return relatorios_nao_cadastrados

#         except Exception as e:
#             print(f"Erro ao consultar os relatórios não cadastrados: {e}")
#             return []
        
#     def consultar_condutor(self, id:int):
#         try:
#             with Session(bind=self.engine) as session:
#                 condutor = session.query(DTP_Condutores).filter(DTP_Condutores.id == id).first()
#                 return condutor
#         except SQLAlchemyError as e:    
#             print(f"Erro ao consultar o condutor: {e}")

#     def consultar_todas_inspecoes(self):
#         try:
#             with Session(bind=self.engine) as session:
#                 inspecoes = session.query(DTP_Inspecoes).all()
#                 return inspecoes
#         except SQLAlchemyError as e:
#             print(f"Erro ao consultar todas as inspeções: {e}")
#             return None
        
#     def consultar_inspecao(self, numero_relatorio:int):
#         try:
#             with Session(bind=self.engine) as session:
#                 inspecao = session.query(DTP_Inspecoes).filter(DTP_Inspecoes.numero_relatorio == numero_relatorio).first()
#                 if inspecao:
#                     return inspecao
#                 else:
#                     print(f"Inspeção {numero_relatorio} não encontrada!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao consultar a inspeção: {e}")

#     def consultar_dtp_stats(self, ano:int, mes:int, modalidade:str):
#         try:
#             stats = []
#             with Session(bind=self.engine) as session:
#                 modalidades = session.query(DTP_Stats.modalidade).distinct().all()
#                 for modalidade in modalidades:
#                     dados = session.query(DTP_Stats).filter(DTP_Stats.ano == ano, DTP_Stats.mes == mes, DTP_Stats.modalidade == modalidade).first()
#                     if stats:
#                         stats.append(dados)
#                     else:
#                         print(f"Stats do ano {ano}, mês {mes} e modalidade {modalidade}  não encontrados!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao consultar as stats: {e}")
        
#     # CRUD - Update
#     def atualizar_relatorio(self, numero_relatorio:int, status_relatorio:str):
#         try:
#             with Session(bind=self.engine) as session:
#                 relatorio = session.query(DTP_Relatorios).filter(DTP_Relatorios.numero_relatorio == numero_relatorio).first()
#                 if relatorio:
#                     relatorio.numero_relatorio = numero_relatorio
#                     relatorio.status_relatorio = status_relatorio
#                     session.commit()
#                     print(f"Relatório {numero_relatorio} atualizado com sucesso!")
#                 else:
#                     print(f"Relatório {numero_relatorio} não encontrado!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao atualizar o relatório: {e}")

#     def atualizar_condutor(self, id: int, nome_condutor: str, telefone_condutor: str, status_whatsapp: str):
#         try:
#             with Session(bind=self.engine) as session:
#                 condutor = session.query(DTP_Condutores).filter(DTP_Condutores.id == id).first()
#                 if condutor:
#                     condutor.nome = nome_condutor
#                     condutor.telefone = telefone_condutor
#                     condutor.status_whatsapp = status_whatsapp
#                     session.add(condutor)  # Adicione essa linha
#                     session.commit()
#                     print(f"Condutor {telefone_condutor} atualizado com sucesso!")
#                 else:
#                     print(f"Condutor {telefone_condutor} não encontrado!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao atualizar o condutor: {e}")
#     def atualizar_inspecao(self, placa:str, numero_relatorio:int, modalidade:str, aprovacao:datetime, validade_crm_alvara:datetime, nome_condutor:str, telefone_condutor:str, status_whatsapp:str):
#         try:
#             with Session(bind=self.engine) as session:
#                 inspecao = session.query(DTP_Inspecoes).filter(DTP_Inspecoes.numero_relatorio == numero_relatorio).first()
                
#                 if inspecao:
#                     condutor_id, nome_condutor, telefone_condutor, status_whatsapp = self.cadastrar_condutor(nome_condutor, telefone_condutor, status_whatsapp)
#                     inspecao.placa = placa
#                     inspecao.modalidade = modalidade
#                     inspecao.data_aprovacao = aprovacao
#                     inspecao.validade_crm_alvara = validade_crm_alvara
#                     inspecao.condutor_id = condutor_id
#                     session.commit()
#                     print(f"Inspeção {numero_relatorio} atualizada com sucesso!")
#                 else:
#                     print(f"Inspeção {numero_relatorio} não encontrada!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao atualizar a inspeção: {e}")

#     # CRUD - Delete
#     def excluir_relatorio(self, numero_relatorio:int):
#         try:
#             with Session(bind=self.engine) as session:
#                 relatorio = session.query(DTP_Relatorios).filter(DTP_Relatorios.numero_relatorio == numero_relatorio).first()
#                 if relatorio:
#                     session.delete(relatorio)
#                     session.commit()
#                     print(f"Relatório {numero_relatorio} excluído com sucesso!")
#                 else:
#                     print(f"Relatório {numero_relatorio} não encontrado!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao excluir o relatório: {e}")

#     def excluir_condutor(self, id:int):
#         try:
#             with Session(bind=self.engine) as session:
#                 condutor = session.query(DTP_Condutores).filter(DTP_Condutores.id == id).first()
#                 if condutor:
#                     session.delete(condutor)
#                     session.commit()
#                     print(f"Condutor {id} excluído com sucesso!")
#                 else:
#                     print(f"Condutor {id} não encontrado!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao excluir o condutor: {e}")

#     def excluir_inspecao(self, numero_relatorio:int):
#         try:
#             with Session(bind=self.engine) as session:
#                 inspecao = session.query(DTP_Inspecoes).filter(DTP_Inspecoes.numero_relatorio == numero_relatorio).first()
#                 relatorio = session.query(DTP_Relatorios).filter(DTP_Relatorios.numero_relatorio == numero_relatorio).first()
#                 if inspecao and relatorio:
#                     session.delete(inspecao)
#                     session.delete(relatorio)
#                     session.commit()
#                     print(f"Inspeção {numero_relatorio} excluida com sucesso!")
#                 else:
#                     print(f"Inspeção {numero_relatorio} não encontrada!")
#         except SQLAlchemyError as e:
#             print(f"Erro ao excluir a inspeção: {e}")
                

# if __name__ == '__main__':
#     g = GerenciadorDTP()
#     g.cadastrar_relatorio(1234)
