import os
import time
import subprocess
import psutil
from tkinter import messagebox

def checar_bitlocker():
    # Chama o manage-bde para verificar o status do BitLocker no drive
    checa_criptografia = subprocess.run(['manage-bde', '-status', os.getcwd()[0:2]], capture_output=True, text=True)

    # Verifica se a checagem deu erro
    if checa_criptografia.returncode != 0:
        messagebox.showinfo("ERRO", "Ocorreu um erro inesperado!")

    # Checa o status da criptografia no drive
    output = checa_criptografia.stdout
    if "Protection On" in output:
        checa_id = subprocess.run("manage-bde -protectors -get " + os.getcwd()[0:2], capture_output=True, text=True, shell=True)

        if checa_id.returncode == 0:
            key_id = ""

            for linha in checa_id.stdout.splitlines():
                if "ID" in linha:
                    key_id = linha.split(":")[1].strip()
                    break

            if key_id == "suaChaveIDAqui":
                retornar_credenciais()
            else:
                recadastrar()
                messagebox.showinfo("ERRO", "O Bitlocker foi modificado, Será necessário recadastrar o usuário! (basta abrir o programa novamente)")
        else:
            recadastrar()
            messagebox.showinfo("ERRO", "Houve um erro, será necessário recadastrar o usuário! (basta abrir o programa novamente)")
    elif "Protection Off" in output:
        recadastrar()
        messagebox.showinfo("ERRO", "Drive não está com o BitLocker ativo, será necessário recadastrar o usuário! (basta abrir o programa novamente)")


def retornar_credenciais():
    # Verifica se quem está executando é o arquivo de interface, se sim retorna os dados
    if "bats-fiap-main\\project\\interface.py" in psutil.Process(psutil.Process(os.getppid()).ppid()).cmdline()[1]:
        print("< 0 >")
        print("  |  ")
        print(" [ ] ")
    else:
        recadastrar()
        messagebox.showinfo("ERRO","Houve um erro, será necessário recadastrar o usuário! (basta abrir o programa novamente)")


def recadastrar():
    # Detecta se o caminho da credencial existe, se sim o apaga
    if os.path.exists(os.getcwd()[0:2] + "\\bats-fiap-main\\scripts\\Credentials"):
        time.sleep(0.1)
        os.system('start cmd /c rd /s /q \"' + os.getcwd()[0:2] + '\\bats-fiap-main\\scripts\\Credentials\"')


checar_bitlocker()
