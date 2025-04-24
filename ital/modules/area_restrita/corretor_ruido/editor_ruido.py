from ital.modules.area_restrita.corretor_ruido.gerador_dados_ruido import GeradorDadosRuido
from rede.rede_compartilhada import PC_ANALISADOR
import os 
import subprocess
from time import sleep
from keyboard import press_and_release, write
import pyautogui as pg
from datetime import datetime
import shutil
from random import randint


class EditorRuido():
    
    def __init__(self, dir_editor, gerador, temp_motor, temp_ar, posicao_motor, pressao_atm, velocidade_vento, posicao_escapamento, qtd_escapamentos, valor_ultimo_ajuste, data_ultimo_ajuste, hora_ultimo_ajuste, inicio_teste, fim_teste):
        self.dir_editor = dir_editor
        # Dados veiculo
        self.numero_ficha = gerador.numero_ficha
        self.placa = gerador.placa

        # Coluna 1
        self.ruidos_acel = gerador.gui_lista_ruido_acel
        self.ruidos_ml = gerador.gui_lista_ruido_ml
        self.rf1 = gerador.rf1
        self.rf2 = gerador.rf2
        self.mediana = gerador.mediana
        self.mediana_corrigida = gerador.mediana_corrigida
        self.variacao = gerador.variacao
        self.p20 = str(gerador.p20) + '0'
        self.limite_ruido = gerador.limite_ruido
        self.qtd_escapamentos = qtd_escapamentos
        self.rpm_ensaio = gerador.rpm_ensaio
        self.rpm_ml_min = gerador.rpm_ml - 200
        self.rpm_ensaio_min = gerador.rpm_ensaio - 200
        self.velocidade_vento = velocidade_vento
        self.resultado = gerador.resultado.upper()

        # Coluna 2
        self.rpms_acel = gerador.gui_lista_rpm_acel
        self.rpms_ml = gerador.gui_lista_rpm_ml
        self.rpm_ml_max = gerador.rpm_ml + 200
        self.rpm_ensaio_max = gerador.rpm_ensaio + 200

        # Observações
        self.temp_motor = temp_motor
        self.temp_ar = temp_ar
        self.pressao_atm = pressao_atm
        self.rpm_ml = randint(self.rpm_ml_min, self.rpm_ml_max)
        self.rpm_potencia_max = int((gerador.rpm_ensaio / 0.75))
        self.posicao_motor = posicao_motor
        self.posicao_escapamento = posicao_escapamento
        self.valor_ultimo_ajuste = valor_ultimo_ajuste
        self.data_ultimo_ajuste = data_ultimo_ajuste.strftime('%d/%m/%Y')
        self.hora_ultimo_ajuste = hora_ultimo_ajuste
        self.inicio_teste = inicio_teste
        self.fim_teste = fim_teste
        inicio_teste_datetime = datetime.combine(data_ultimo_ajuste, inicio_teste)
        fim_teste_datetime = datetime.combine(data_ultimo_ajuste, fim_teste)
        self.duracao_teste = '0' + str(fim_teste_datetime - inicio_teste_datetime)

        self.matar_processo()
        self.iniciar_editor()
        self.editar_dados()
        self.editar_observacoes(posx=411, posy=522)

    @staticmethod
    def matar_processo():
        comando = f"taskkill /f /im Executavel.exe"
        subprocess.run(comando, shell=True)
        print('Processo editor finalizado.')
        sleep(0.2)

    @staticmethod
    def escrever_texto(texto:str, delay=0.01):
        for letra in texto:
            write(letra)
            sleep(delay)

    @staticmethod
    def repetir_comando(comando, quantidade:int, delay=0.01):
        for _ in range(quantidade):
            press_and_release(comando) 
            sleep(delay)

    @staticmethod
    def backup_ficha(dir_backup):
        shutil.copy2()

    def iniciar_editor(self):
        password = 'cba'
        # Abrir o editor
        subprocess.Popen(self.dir_editor)
        sleep(0.5)
        self.escrever_texto(password)
        sleep(0.5)
        press_and_release('enter')
        press_and_release('enter')
        sleep(0.5)

        # Selecionar ficha
        press_and_release('alt')
        press_and_release('right arrow')
        press_and_release('right arrow')
        press_and_release('enter')
        sleep(0.5)
        self.escrever_texto(str(self.numero_ficha))
        press_and_release('enter')
        press_and_release('tab')
        press_and_release('right arrow')
        sleep(0.5)
    
    def editar_dados(self):
        # Coluna 1
        for i in range(len(self.ruidos_acel)):
            pg.write(str(self.ruidos_acel[i]))
            press_and_release('down arrow')
            sleep(0.05)
        
        for i in range(len(self.ruidos_ml)):
            pg.write(str(self.ruidos_ml[i]))
            press_and_release('down arrow')
            sleep(0.05)

        lista_validacao = [self.rf1, self.rf2, self.mediana, self.mediana_corrigida, self.variacao, self.p20, self.limite_ruido, self.qtd_escapamentos, self.rpm_ml_min, self.rpm_ensaio_min, self.velocidade_vento, self.resultado]
        for i in range(len(lista_validacao)):
            pg.write(str(lista_validacao[i]))
            press_and_release('down arrow')
            sleep(0.01)

        press_and_release('right arrow')
        for i in range(5):
            press_and_release('page up')
            sleep(0.01)    

        # Coluna 2
        for i in range(len(self.rpms_acel)):
            pg.write(str(self.rpms_acel[i]))
            press_and_release('down arrow')
            sleep(0.01)

        for i in range(len(self.rpms_ml)):
            pg.write(str(self.rpms_ml[i]))
            press_and_release('down arrow')
            sleep(0.01)

        for i in range(8):
            press_and_release('down arrow')
            sleep(0.01)
        
        lista_rpm_max = [self.rpm_ml_max, self.rpm_ensaio_max]
        for i in range(len(lista_rpm_max)):
            pg.write(str(lista_rpm_max[i]))
            press_and_release('down arrow')
            sleep(0.01)
        
        for i in range(2):
            press_and_release('down arrow')
            sleep(0.03)      

    def editar_observacoes(self, posx, posy):
        observacoes = f"""Ensáio conforme conama 418 e instrução normativa n° 6 do ibama
    
1. Condições do teste
a. Temperatura do motor = {str(int(self.temp_motor))} °C
b. Temperatura do ar = {str(int(self.temp_ar))} °C
c. Pressão atmosférica = {self.pressao_atm} KPa
d. Velocidade do vento = {self.velocidade_vento} m/s
e. Rotação de marcha lenta: {self.rpm_ml} RPM
f. Rotação de potência máxima: {self.rpm_potencia_max} RPM
g. Rotação de ensáio: {self.rpm_ensaio} RPM
g. Ruído Maximo: {self.limite_ruido} DB
h. Posição do motor: {self.posicao_motor}
i. Posição do escapamento: {self.posicao_escapamento}
j. N° de escapamentos: {self.qtd_escapamentos}
k. Valor antes do último ajuste: {self.valor_ultimo_ajuste} db
l. Data e hora antes do último ajuste: {self.data_ultimo_ajuste} {self.hora_ultimo_ajuste}
m. Tempo Teste Inicial: {self.inicio_teste}
n. Tempo Teste Final: {self.fim_teste}
o. Tempo Teste: {self.duracao_teste}
----------Inspeção Visual----------
Timbres e níveis de ruído anormais - NÃO
Peças defeituosas e/ou corrídas ou não originais - NÃO
Ausência de componentes - NÃO

"""
        pg.click(posx, posy)
        self.repetir_comando('left arrow', 10)
        self.repetir_comando('up arrow', 10)
        self.repetir_comando('delete', 1100, 0.000001)
        self.repetir_comando('backspace', 5)
        self.escrever_texto(observacoes, 0.001)

            # Grava e Sai
        pg.click(x=903, y=570)
        sleep(0.5)
        pg.click(x=903, y=570)
        sleep(0.5)
        pg.click(x=903, y=570)
        sleep(0.15)
        pg.click(x=329, y=563)
        sleep(0.15)
        pg.click(x=462, y=567)
        sleep(0.15)
            


    

if __name__ == '__main__':
    dados = GeradorDadosRuido(9701, 'ABC1234', 85.23, 4500, 850, resultado='APROVADO', qtd_leituras=5)
    editor = EditorRuido(r"\\SERVIDOR-PC\Arquivos\03. Vitor\Executavel.exe", dados)
   
