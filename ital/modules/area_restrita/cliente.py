from flask import Flask, request, jsonify
import subprocess
import os
from time import sleep
from keyboard import press_and_release
from pyautogui import write

app = Flask(__name__)

# Caminho fixo do .exe na área de trabalho
def get_exe_path_cliente():
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    print(path)
    return os.path.join(path, "Executavel.exe")

def escrever_texto(texto):
    for caractere in texto:
        write(caractere)
        sleep(0.05)

@app.route('/executar', methods=['POST'])
def executar_exe():
    data = request.json
    numero_ficha = data.get('numero_ficha')
    senha = data.get('senha', 'cba')

    try:
        subprocess.Popen(get_exe_path_cliente())
        sleep(0.5)
        escrever_texto(senha)
        press_and_release('enter')
        press_and_release('enter')
        sleep(0.5)

        # Simulação de uso com número da ficha
        press_and_release('alt')
        press_and_release('right arrow')
        press_and_release('right arrow')
        press_and_release('enter')
        sleep(0.5)
        escrever_texto(str(numero_ficha))
        press_and_release('enter')
        press_and_release('tab')
        press_and_release('right arrow')

        return jsonify({"status": "executado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
