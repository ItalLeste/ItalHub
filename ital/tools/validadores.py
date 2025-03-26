"""
Módulo responsável por validar os dados de entrada.
"""
import re

def validar_nome_completo(v:str):
    if not v.isalpha():
        raise ValueError("Nome inválido. Deve conter apenas letras.")
    return v.capitalize()

def validar_placa(v:str):
    v = v.replace(" ", "").replace("-", "") # Remove espaços, traços.
    if len(v) != 7:
        raise ValueError("Placa inválida. Deve conter exatamente 7 caracteres.")
    if not (v[:3].isalpha() and v[3].isdigit() and v[5:].isdigit()):
        raise ValueError("Placa inválida. Os 3 primeiros caracteres devem ser letras, o quarto e os 2 últimos caracteres devem ser números.")
    if not (v[4].isdigit() or (v[4].isalpha() and v[4] <= 'J')):
        raise ValueError("Placa inválida. O caractere na posição 5 deve ser um número ou uma letra (A-J).")
    return v.upper()

def validar_numero_relatorio(v:str):
    try:
        v = int(v)
    except ValueError:
        raise ValueError("Número de relatório inválido. Deve ser um número inteiro.")
    if v <= 0:
        raise ValueError("Número de relatório inválido. Deve ser maior que zero.")

    return v    

def validar_telefone(v:str):
    v = re.sub(r'\D', '', v)  # remove todos os caracteres não numéricos
    if 9 < len(v) < 11:
        print(len(v))
        raise ValueError("Telefone inválido. Deve conter entre 9 e 11 caracteres.")
    return v
    
