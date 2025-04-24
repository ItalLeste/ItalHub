"""
    Esta classe é responsável por gerar os dados de um ensaio de ruído para a ficha informada.

    Returns: Objeto de classe com os atributos.
"""
import random
from statistics import mean, median
from math import log10
from ital.tools.validadores import validar_placa

class GeradorDadosRuido():
    VALORES_LEITURA_PERMITIDOS = [5, 7, 9]
    RUIDO_FUNDO_MINIMO = 63.00
    RUIDO_FUNDO_MAXIMO = 67.00
    RPM_ML_MINIMO = -150
    RPM_ML_MAXIMO = 150
    RPM_ACEL_MINIMO = -150    
    RPM_ACEL_MAXIMO = 150
    FATOR_CORRECAO_RUIDO_ML = 0.77
    RUIDO_ACEL_MINIMO = -2.5
    RUIDO_ACEL_MAXIMO = 0.5
    RUIDO_ML_MINIMO = -2
    RUIDO_ML_MAXIMO = 1

    def __init__(self, numero_ficha:int, placa:str, limite_ruido:float, rpm_ensaio:float, rpm_ml:int, resultado:str='APROVADO', qtd_leituras:int=5):
        # Validação Dados
        if not numero_ficha.is_integer():
            raise ValueError('Número da ficha deve ser um número inteiro.')
        
        validar_placa(placa)
        
        if qtd_leituras not in self.VALORES_LEITURA_PERMITIDOS:
            raise ValueError(f'Quantidade de leituras permitidas: {self.VALORES_LEITURA_PERMITIDOS}')
        
        resultado = resultado.upper()

        if resultado not in ['APROVADO', 'REPROVADO']:
            raise ValueError('Resultado permitido: APROVADO ou REPROVADO')
        
        if resultado == 'REPROVADO': # Transforma os dados.
            qtd_leituras = 5
            self.RUIDO_ACEL_MAXIMO = 4
            self.RUIDO_ML_MINIMO = 0
            self.RUIDO_ML_MAXIMO = 1
            self.RUIDO_ACEL_MINIMO = 0
            
        self.numero_ficha = numero_ficha
        self.placa = placa
        self.limite_ruido = limite_ruido 
        self.rpm_ensaio = rpm_ensaio
        self.rpm_ml = rpm_ml   
        self.resultado = resultado
        self.qtd_leituras = qtd_leituras
        self.rf1, self.rf2 = self.gerar_ruido_fundo()
        self.lista_rpm_ml = self.gerar_rpm_ml()
        self.lista_rpm_acel = self.gerar_rpm_acel()
        self.lista_ruido_ml = self.gerar_ruido_ml()
        self.lista_ruido_acel = self.gerar_ruido_acel()
        self.ordenar_listas()
        self.mediana, self.variacao, self.ma, self.mp = self.calcular_mediana()
        self.p20 = self.calcular_p20()
        self.mediana_corrigida = self.calcular_mediana_corrigida()
        self.agrupar_dados()
        self.validar_resultado()

    def gerar_intervalos(self, minimo, maximo):
        """Gera uma lista de deslocamentos de 0.5 em 0.5 dentro de um intervalo."""
        atual = minimo
        while atual <= maximo:
            yield round(atual, 2)
            atual += 0.5

    def gerar_ruido_fundo(self):
        # Gera todos os valores possíveis (de 0.5 em 0.5)
        valores_possiveis = [round(self.RUIDO_FUNDO_MINIMO + i * 0.5, 2) for i in range(int((self.RUIDO_FUNDO_MAXIMO - self.RUIDO_FUNDO_MINIMO) / 0.5) + 1)]
        
        # Sorteia UM valor para rf1 e UM valor para rf2
        rf1 = random.choice(valores_possiveis)
        rf2 = random.choice(valores_possiveis)
        return rf1, rf2
    
    def gerar_rpm_ml(self):
        self.lista_rpm_ml = []
        rpm = self.rpm_ml
        ml_s = self.RPM_ML_MAXIMO
        ml_i = self.RPM_ML_MINIMO
        valores_possiveis = [int(rpm + delta) for delta in self.gerar_intervalos(ml_i, ml_s)]

        for _ in range(self.qtd_leituras + 2):
            v = random.choice(valores_possiveis)
            self.lista_rpm_ml.append(v)
        return self.lista_rpm_ml
    
    def gerar_rpm_acel(self):
        self.lista_rpm_acel = []
        rpm = self.rpm_ensaio
        ml_s = self.RPM_ACEL_MAXIMO
        ml_i = self.RPM_ACEL_MINIMO
        valores_possiveis = [int(rpm + delta) for delta in self.gerar_intervalos(ml_i, ml_s)]
       
        for _ in range(self.qtd_leituras):
            v = random.choice(valores_possiveis)
            self.lista_rpm_acel.append(v)
        return self.lista_rpm_acel
    
    def gerar_ruido_ml(self):
        self.lista_ruido_ml = []
        r = self.limite_ruido * self.FATOR_CORRECAO_RUIDO_ML # Ruido em marcha lenta.
        r = round(round(r * 2) / 2, 2) # Arrenda o valor para .00 ou .50
        r_min = self.RUIDO_ML_MINIMO
        r_max = self.RUIDO_ML_MAXIMO
        valores_possiveis = [round(r + delta, 2) for delta in self.gerar_intervalos(r_min, r_max)] # Gera lista de valores possíveis de 0.5 em 0.5
        
        for _ in range(self.qtd_leituras + 2):
            v = random.choice(valores_possiveis)
            self.lista_ruido_ml.append(v)

        return self.lista_ruido_ml

    def gerar_ruido_acel(self):
        self.lista_ruido_acel = []
        r = round(round(self.limite_ruido * 2) / 2, 2) # Arrenda o valor para .00 ou .50
        r_min = self.RUIDO_ACEL_MINIMO
        r_max = self.RUIDO_ACEL_MAXIMO
        valores_possiveis = [round(r + delta, 2) for delta in self.gerar_intervalos(r_min, r_max)]

        # Incrementa o valor obtido durante a leitura a fim de forçar mais uma leitura.
        for i in range(self.qtd_leituras):
            v = random.choice(valores_possiveis)
            if self.qtd_leituras == 7:
                if i == 0:
                    v + 2.5
                elif i == 1:
                    v + 2
            
            elif self.qtd_leituras == 9:
                if i < 3:
                    v += 3.5 - i
            self.lista_ruido_acel.append(v)

        return self.lista_ruido_acel
    
    # Validação de Dados
    def ordenar_listas(self):
        # ordena as listas de dados em ordem cresce (lo -> lista ordenada)
        self.lo_rpm_ml = sorted(self.lista_rpm_ml)
        self.lo_rpm_acel = sorted(self.lista_rpm_acel)
        self.lo_ruido_ml = sorted(self.lista_ruido_ml)        
        self.lo_ruido_acel = sorted(self.lista_ruido_acel)
        return self.lo_rpm_ml, self.lo_rpm_acel, self.lo_ruido_ml, self.lo_ruido_acel

    def calcular_mediana(self):
        self.mediana = median(self.lo_ruido_acel)
        mediana_indice = round(len(self.lo_ruido_acel) / 2)

        print(f'Mediana: {self.mediana}')
        print(f'Indice da Mediana: {mediana_indice}')

        self.ma = self.lo_ruido_acel[mediana_indice - 1]
        self.mp = self.lo_ruido_acel[mediana_indice + 1]	
        self.variacao = self.mp - self.ma
        print(f'Variação: {self.variacao}')
        return self.mediana, self.variacao, self.ma, self.mp
    
    def calcular_p20(self):
        self.lo_ruido_ml.append(self.rf1)
        self.lo_ruido_ml.append(self.rf2)
        l = sorted(self.lo_ruido_ml)
        n = len(l)
        x = round((0.2 * (n - 1) + 1), 2) # Arredonda a valor encontrado na equação.
        k = int(x)
        d = round(x - k, 2)

        if 0 < k < n:
            self.p20 = l[k-1] + (d * (l[k] - l[k-1]))
            return self.p20
        if k == 0:
            self.p20 = l[0]
            return self.p20
        if k == n:
            self.p20 = l[n]
            return self.p20
    
    def calcular_mediana_corrigida(self):
        d = self.mediana - self.p20
        if 10 > d > 3 and  self.mediana > self.limite_ruido:
            ra = mean(self.rf1, self.rf2) # Média dos ruidos de fundo.
            rm = median(self.lo_ruido_acel) # Mediana dos ruidos de aceleração ordenados.
            self.mediana_corrigida = 10 * log10((10 ** (rm / 10) - 10 ** (ra / 10)))
        else:
            self.mediana_corrigida = self.mediana
        return self.mediana_corrigida
    
    def validar_resultado(self):
        while True:
            if not (self.mediana_corrigida <= self.limite_ruido and 0 <= self.variacao <= 2):
                print(f'Validação de Dados: Resultado inválido, gerando novos dados...')
                print(f'Mediana Corrigida: {self.mediana_corrigida}')
                print(f'Variação: {self.variacao}')
                print(f'Ruido Acel Ordenado: {self.lo_ruido_acel}')        
                
                indice = round((len(self.lista_ruido_acel)+1)/2) # Inicio pelo meio da lista.
                print(f'Índice da Mediana: {indice}')
                self.ajustar_dados(indice)
                indice += 1 # Caso a condição nao seja setisfeita, modifica o próximo indice até completar a tabela.

                print(f'Novo RPM Acel Ordenado: {self.lo_ruido_acel}')
                print(f'Nova Mediana Corrigida: {self.mediana_corrigida}')
                print(f'Novo Variação: {self.variacao}')
                print('------------------------------------------------------------')
                break
            
            else:
                print()
                print('**** Validação de Dados ****')
                print(f'Resultado: {self.resultado}')
            #     print(f'Mediana Corrigida: {self.mediana_corrigida} dB')
            #     print(f'Variação: {self.variacao}')

            #     print(f'Limite de Ruido: {self.limite_ruido} dB')
            #     print(f'Quantidade de Leituras: {self.qtd_leituras}')

            #     print(f'Ruído em Aceleração: {self.gui_lista_ruido_acel}')
            #     print(f'RPM em Aceleração: {self.gui_lista_rpm_acel}')
            #     print(f'Ruído em ML: {self.gui_lista_ruido_ml}')
            #     print(f'RPM em ML: {self.gui_lista_rpm_ml}')

            #     print(f'Fundo 1: {self.rf1} dB')
            #     print(f'Fundo 2: {self.rf2} dB')
            #     print(f'Mediana: {self.mediana} dB')
            #     print(f'Mediana corrigida: {self.mediana_corrigida} dB')
            #     print(f'P20: {self.p20} dB')
            #     print(f'Variação: {self.variacao} dB')
                print()
                return True

    def ajustar_dados(self, indice:int):
        print(f'Medida Posterior à Mediana: {self.mp}')
        self.lista_ruido_acel[self.mp] = self.lista_ruido_acel[indice]
        self.ordenar_listas()
        self.mediana, self.variacao = self.calcular_mediana()
        self.p20 = self.calcular_p20()
        self.mediana_corrigida = self.calcular_mediana_corrigida()

    # Agrupar Dados para Automação
    def agrupar_dados(self):
        self.gui_lista_rpm_acel = []
        self.gui_lista_rpm_ml = []
        self.gui_lista_ruido_acel = []
        self.gui_lista_ruido_ml = []
        for i in range(10):
            if i < self.qtd_leituras:
                self.gui_lista_rpm_acel.append(self.lista_rpm_acel[i])
                self.gui_lista_ruido_acel.append(self.lista_ruido_acel[i])
            else:
                self.gui_lista_rpm_acel.append('---')
                self.gui_lista_ruido_acel.append('---')
                
            if i < self.qtd_leituras + 1:
                self.gui_lista_rpm_ml.append(self.lista_rpm_ml[i])
                self.gui_lista_ruido_ml.append(self.lista_ruido_ml[i])
            else:
                self.gui_lista_rpm_ml.append('---')
                self.gui_lista_ruido_ml.append('---')

        return self.gui_lista_rpm_acel, self.gui_lista_rpm_ml, self.gui_lista_ruido_acel, self.gui_lista_ruido_ml


if __name__ == '__main__':
    gerador = GeradorDadosRuido(1, 'ABC1234', 85.23, 4500, 850, resultado='APROVADO', qtd_leituras=5)
  