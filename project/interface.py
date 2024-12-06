# FIAP AUTOLAB
# IMPORTANTE: se você achou este pen drive, NAO EXECUTE OS COMANDOS, eles servem
# Unica e exclusivamente para auxilio de monitores, utiliza-los indevidamente pode acarretar
# em problemas serios.
# Creditos:
# Victor Flavio Demarchi Viana
# Ryan Brito Pereira Ramos


# Bibliotecas
import os
import sys
import subprocess
import socket
import threading
import time
from tkinter import Canvas, PhotoImage, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import customtkinter
from PIL import Image, ImageTk
import ctypes

# Caminho do projeto
path = __file__.split("\\")
main = path[0] + f"\\{path[1]}\\"

sys.path.append(path[1])

# Subpastas do projeto
autolab = main + "autolab\\"
project = main + "project\\"
scripts = main + "scripts\\"
assets = project + "assets\\"

from autolab import screens, password, action

# Credenciais
nome_user = ""
login_user = ""
senha_user = ""

# connected_ips = set()

# Icone da barra de tarefas da aplicação (Windows)
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Tema
customtkinter.set_appearance_mode("dark")

# Fontes e Cores
fonte = ("Arial", 18, "bold")
fontePequena = ("Arial", 12, "bold")
fonteBotao = ("Arial", 16, "bold")
fonteBotaoP = ("Arial", 14, "bold")
cor_fundo = "#ed145b"
cor_fundo_escuro = "#d01150"
cor_input = "#242424"
cor_input_numerico = "#565b5e"
cor_fonte_input_numerico = "#9e9e9e"
cor_fundo_input_numerico = "#1c2022"
hover_input_numerico = "#040505"
cor_continuar = "#039A2B"
cor_continuar_escuro = "#027C23"
cor_voltar = "#D90404"
cor_voltar_escuro = "#BC0404"

# Variaveis globais para controle do estado dos botoes
incrementing = False
decrementing = False


def recadastrar():
    # Detecta se o caminho da credencial existe, se sim o apaga
    if os.path.exists(scripts + "credentials.bin"):
        os.remove(scripts + "credentials.bin")


# Checagens
def checar_bitlocker():
    # Chama o manage-bde para verificar o status do BitLocker no drive
    result = subprocess.run(['manage-bde', '-status', os.getcwd()[0:2]], capture_output=True, text=True)

    # Verifica se a checagem deu erro
    if result.returncode != 0:
        recadastrar()
        messagebox.showinfo("ERRO", "Ocorreu um erro inesperado!")

    # Checa o status da criptografia no drive
    output = result.stdout
    if "Protection On" in output:
        checar_authenticator()
    elif "Protection Off" in output:
        recadastrar()
        messagebox.showinfo("ERRO", "Drive não está com o BitLocker ativo!")


# def handle_client(client_socket, client_address):
#     connected_ips.add(client_address[0])
#     client_socket.close()
#
# def coletarIps():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(("0.0.0.0", 12345))
#     server_socket.listen(5)
#
#     while True:
#         client_socket, client_address = server_socket.accept()
#
#         client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
#         client_thread.start()

def pegar_chave_bitlocker():
    # Pega a chave do Bitlocker para garantir que é a mesma do usuário cadastrado
    resultado = subprocess.run("manage-bde -protectors -get " + os.getcwd()[0:2], capture_output=True, text=True,
                               shell=True)

    # Checa se a operação acima não deu erro e coleta a chave ID
    if resultado.returncode == 0:
        for linha in resultado.stdout.splitlines():
            if "ID" in linha:
                key_id = linha.split(":")[1].strip()
                return key_id
        return None
    else:
        print(f"Error: {resultado.stderr}")
        return None


def criptografa_arquivo(conteudo, arquivo_final, chave):
    # Gera um vetor de inicialização aleatório de 16 bytes
    vi = os.urandom(16)

    # Cria a sifra usando o algoritmo AES, junto a chave
    sifra = Cipher(algorithms.AES(chave), modes.CBC(vi), backend=default_backend())
    encriptador = sifra.encryptor()

    # Preenche o arquivo para o tamanho correto
    enchimento = padding.PKCS7(algorithms.AES.block_size).padder()
    conteudo_com_enchimento = enchimento.update(conteudo.encode()) + enchimento.finalize()

    # Criptografa o arquivo
    conteudo_criptografado = encriptador.update(conteudo_com_enchimento) + encriptador.finalize()

    # Cria um novo arquivo com o conteúdo criptografado
    with open(scripts + arquivo_final, 'wb') as arqv:
        arqv.write(vi)  # Vetor de inicialização sempre no começo
        arqv.write(conteudo_criptografado)


def descriptografa_arquivo(arquivo, chave):
    # Lê o arquivo criptografado
    with open(scripts + arquivo, 'rb') as arqv:
        vi = arqv.read(16)  # Vetor de inicialização no começo
        conteudo_criptografado = arqv.read()  # conteúdo criptografado

    try:
        # Cria a sifra usando o algoritmo AES, junto a chave
        sifra = Cipher(algorithms.AES(chave), modes.CBC(vi), backend=default_backend())
        encriptador = sifra.decryptor()

        # Descriptografa o conteúdo do arquivo
        conteudo_descriptografado = encriptador.update(conteudo_criptografado) + encriptador.finalize()

        # Remove o preenchimento e retorna o conteúdo descriptografado
        remove_preenchimento = padding.PKCS7(algorithms.AES.block_size).unpadder()
        conteudo_original = remove_preenchimento.update(conteudo_descriptografado) + remove_preenchimento.finalize()

        return conteudo_original

    except Exception:
        recadastrar()
        messagebox.showinfo("ERRO", "Ocorreu um erro ao ler as credenciais, usuário deverá ser recadastrado!")
        exit()


def checar_authenticator():
    if os.path.exists(scripts + "credentials.bin"):
        global nome_user, login_user, senha_user

        resultado = descriptografa_arquivo("credentials.bin", hashlib.sha256(pegar_chave_bitlocker().encode()).digest())

        nome_user, login_user, senha_user = resultado.decode().split("\n")

        telaPrincipal(nome_user)
    else:
        tela_login()


# Função para criar arquivo criptografado com credenciais
def cadastrar_monitor(nome, login, senha):
    chave = hashlib.sha256(pegar_chave_bitlocker().encode()).digest()
    criptografa_arquivo(nome + "\n" + login + "\n" + senha, "credentials.bin", chave)


def auto_runas(login, senha):
    if os.path.exists(scripts + "Authenticator\\Authenticator.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "Authenticator\\Authenticator.py", login, senha],
            check=True)


def auto_copy(inicio, passo, fim, arquivo):
    auto_runas(login_user, senha_user)

    if os.path.exists(scripts + "AutoCopy\\AutoCopy.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoCopy\\AutoCopy.py", str(inicio), str(passo), str(fim),
             str(arquivo)], check=True)


def auto_shutdown(inicio, passo, fim, tempo):
    auto_runas(login_user, senha_user)

    time.sleep(0.5)

    if os.path.exists(scripts + "AutoShutdown\\AutoShutdown.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoShutdown\\AutoShutdown.py", str(inicio),
             str(passo), str(fim), str(tempo)], check=True)


def auto_restart(inicio, passo, fim, tempo):
    auto_runas(login_user, senha_user)

    time.sleep(0.5)

    if os.path.exists(scripts + "AutoRestart\\AutoRestart.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoRestart\\AutoRestart.py", str(inicio),
             str(passo), str(fim), str(tempo)], check=True)


def auto_rd(inicio, passo, fim):
    auto_runas(login_user, senha_user)

    time.sleep(0.5)

    if os.path.exists(scripts + "AutoRD\\AutoRD.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoRD\\AutoRD.py", str(inicio),
             str(passo), str(fim)], check=True)


def auto_login(inicio, passo, fim, login, senha):
    auto_runas(login_user, senha_user)

    time.sleep(0.5)

    if os.path.exists(scripts + "AutoLogin\\AutoLogin.py") and os.path.exists(scripts + "AutoUser\\AutoUser.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoLogin\\AutoLogin.py",str(inicio),
             str(passo), str(fim), str(login), str(senha)], check=True)


def auto_message(inicio, passo, fim, mensagem):
    auto_runas(login_user, senha_user)

    time.sleep(0.5)

    if os.path.exists(scripts + "AutoMessage\\AutoMessage.py") and os.path.exists(scripts + "AutoMessage\\AutoMessage.py"):
        subprocess.run(
            [main + "venv\\Scripts\\python.exe", scripts + "AutoMessage\\AutoMessage.py", str(inicio),
             str(passo), str(fim), str(mensagem)], check=True)

# Função generica para aumentar o valor de qualquer campo
def increment_value(entry_widget):
    if incrementing:
        current_value = int(entry_widget.get())
        entry_widget.delete(0, customtkinter.END)
        entry_widget.insert(0, str(current_value + 1))
        janela.after(100, lambda: increment_value(entry_widget))


# Função generica para diminuir o valor de qualquer campo
def decrement_value(entry_widget):
    if decrementing:
        current_value = int(entry_widget.get())
        if current_value > 1:
            entry_widget.delete(0, customtkinter.END)
            entry_widget.insert(0, str(current_value - 1))
        else:
            messagebox.showerror("ERRO", "O valor deve ser maior que 0.")
            entry_widget.delete(0, customtkinter.END)
            entry_widget.insert(0, "1")
        janela.after(100, lambda: decrement_value(entry_widget))


# Funções para iniciar o incremento ou decremento
def start_increment(event, entry_widget):
    global incrementing
    incrementing = True
    increment_value(entry_widget)


def stop_increment(event):
    global incrementing
    incrementing = False


def start_decrement(event, entry_widget):
    global decrementing
    decrementing = True
    decrement_value(entry_widget)


def stop_decrement(event):
    global decrementing
    decrementing = False


# Função para validar a entrada (apenas números)
def validate_input(value):
    # Verifica se a entrada é um número ou vazia
    if value.isdigit() or value == "":
        return True
    else:
        return False


# Telas
def telaPrincipal(nome_user):
    """
    --> Função que exibe a tela principal após o login
    :param nome_user: Nome do usuário preenchido na tela de login
    """
    # Janela principal
    global janela
    janela = customtkinter.CTk()

    janela.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janela)

    # Título
    janela.title("FIAP AUTOLAB")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janela, width=655, height=400, bd=-100000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Logo da FIAP
    logoFiap = PhotoImage(file=assets + "fiapLogo.png")
    canvas1.create_image(330, 62, image=logoFiap)

    # Texto AUTOLAB
    autoLab = PhotoImage(file=assets + "autoLAB.png")
    canvas1.create_image(324, 126, image=autoLab)

    # Mensagem de boas-vindas personalizada
    canvas1.create_text(325, 175, text=f"Bem-vindo, {nome_user}!", fill="white", font=("Arial", 20, "bold"))

    # Botões
    botao_desligar = customtkinter.CTkButton(janela, text="Desligar", width=130, height=40, font=fonteBotaoP,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                             command=lambda: [janela.destroy(), telaDesligar()])
    botao_reiniciar = customtkinter.CTkButton(janela, text="Reiniciar", width=130, height=40, font=fonteBotaoP,
                                              fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                              command=lambda: [janela.destroy(), telaReiniciar()])
    botao_limpar = customtkinter.CTkButton(janela, text="Limpar o (D:)", width=130, height=40, font=fonteBotaoP,
                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                           command=lambda: [janela.destroy(), telaLimpar()])
    botao_copiar = customtkinter.CTkButton(janela, text="Copiar Arquivo", width=130, height=40, font=fonteBotaoP,
                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                            command = lambda: [janela.destroy(), telaCopiar()])
    botao_pon = customtkinter.CTkButton(janela, text="Logar PON", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                        command=lambda: [janela.destroy(), telaPON()])
    botao_pn = customtkinter.CTkButton(janela, text="Logar PN", width=130, height=40, font=fonteBotaoP,
                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                       command=lambda: [janela.destroy(), telaPN()])
    botao_nac = customtkinter.CTkButton(janela, text="Abrir NAC", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_mensagem = customtkinter.CTkButton(janela, text="Mensagem", width=130, height=40, font=fonteBotaoP,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                             command=lambda: [janela.destroy(), telaMensagem()])
    botao_logar = customtkinter.CTkButton(janela, text="Logar Usuário", width=130, height=40, font=fonteBotaoP,
                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                          command=lambda: [janela.destroy(), telaLogarUsuario()])
    botao_url = customtkinter.CTkButton(janela, text="Abrir URL", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_runas = customtkinter.CTkButton(janela, text="Runas", width=130, height=40, font=fonteBotaoP,
                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                          command=lambda: [auto_runas(login_user, senha_user)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(118, 240, window=botao_desligar)
    canvas1.create_window(118, 290, window=botao_reiniciar)
    canvas1.create_window(118, 340, window=botao_logar)
    canvas1.create_window(258, 240, window=botao_limpar)
    canvas1.create_window(258, 290, window=botao_copiar)
    canvas1.create_window(258, 340, window=botao_url)
    canvas1.create_window(398, 240, window=botao_pon)
    canvas1.create_window(398, 290, window=botao_pn)
    canvas1.create_window(398, 340, window=botao_nac)
    canvas1.create_window(538, 240, window=botao_mensagem)
    canvas1.create_window(538, 290, window=botao_runas)

    # Loop da Janela principal
    janela.mainloop()


def telaDesligar():
    """
    --> Função que exibe a tela com os parâmetros do bat shutdown
    """
    # Janela principal
    janelaDesligar = customtkinter.CTk()

    janelaDesligar.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaDesligar)

    # Título
    janelaDesligar.title("AUTOSHUTDOWN")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaDesligar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem Shutdown
    shutdown = ImageTk.PhotoImage(Image.open(assets + "autoSHUTDOWN.png").resize((460, 36)))
    canvas1.create_image(328, 50, image=shutdown)

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaDesligar.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 165, window=entry4)
    canvas1.create_window(525, 200, window=entry5)
    canvas1.create_window(525, 235, window=entry6)
    canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    increase_button = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(185, 235, window=increase_button)
    increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(55, 235, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 268, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 268, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Desligar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 165, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 165, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    increase_button_machine = customtkinter.CTkButton(janelaDesligar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaDesligar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Desligar Lab
    canvas1.create_text(120, 170, text="Desligar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Desligar Lab Inteiro
    botao_desligar_lab_inteiro = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [
                                                             action.executar_acao("Desligar", "Lab", tempo=entry.get()),
                                                             auto_shutdown(1, 1, 99, entry.get()),
                                                             screens.mostrar_comando_executado(
                                                                 janelaDesligar,
                                                                 telaDesligar)])
    # Desligar Máquina
    canvas1.create_text(323, 140, text="Desligar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_desligar_maquina = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50, font=fonte,
                                                     fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                     command=lambda: [action.executar_acao("Desligar", "Maquina",
                                                                                           maquina=entry2.get(),
                                                                                           tempo=entry3.get()),
                                                                      auto_shutdown(entry2.get(), 1, entry2.get(),
                                                                                    entry3.get()),
                                                                      screens.mostrar_comando_executado(janelaDesligar,
                                                                                                        telaDesligar)])

    # Desligar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_desligar_personalizado = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50,
                                                           font=fonte,
                                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                           command=lambda: [
                                                               action.executar_acao("Desligar", "Personalizado",
                                                                                    inicio=entry4.get(),
                                                                                    fim=entry5.get(),
                                                                                    passo=entry6.get(),
                                                                                    tempo=entry7.get()),
                                                               auto_shutdown(entry4.get(), entry6.get(), entry5.get(),
                                                                             entry7.get()),
                                                               screens.mostrar_comando_executado(
                                                                   janelaDesligar,
                                                                   telaDesligar)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 285, window=botao_desligar_lab_inteiro)
    canvas1.create_window(323, 319, window=botao_desligar_maquina)
    canvas1.create_window(525, 350, window=botao_desligar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaDesligar,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaDesligar.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaDesligar.mainloop()


def telaReiniciar():
    """
    --> Função que exibe a tela com os parâmetros do bat shutdown com o parâmetro -r (reiniciar)
    """
    # Janela principal
    janelaReiniciar = customtkinter.CTk()

    janelaReiniciar.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaReiniciar)

    # Título
    janelaReiniciar.title("AUTORESTART")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaReiniciar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem Shutdown
    restart = ImageTk.PhotoImage(Image.open(assets + "autoRESTART.png"))
    canvas1.create_image(328, 50, image=restart)

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaReiniciar.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaReiniciar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 165, window=entry4)
    canvas1.create_window(525, 200, window=entry5)
    canvas1.create_window(525, 235, window=entry6)
    canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    increase_button = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(185, 235, window=increase_button)
    increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(55, 235, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 268, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 268, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Reiniciar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 165, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 165, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    increase_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaReiniciar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Reiniciar Lab
    canvas1.create_text(120, 170, text="Reiniciar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Reiniciar Lab Inteiro
    botao_reiniciar_lab_inteiro = customtkinter.CTkButton(janelaReiniciar, text="Reiniciar", width=170, height=50,
                                                          font=fonte,
                                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                          command=lambda: [action.executar_acao("Reiniciar", "Lab",
                                                                                                tempo=entry.get()),
                                                                           auto_restart(1, 1, 99, entry.get()),
                                                                           screens.mostrar_comando_executado(
                                                                               janelaReiniciar,
                                                                               telaReiniciar)])
    # Reiniciar Máquina
    canvas1.create_text(323, 140, text="Reiniciar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_reiniciar_maquina = customtkinter.CTkButton(janelaReiniciar, text="Reiniciar", width=170, height=50,
                                                      font=fonte,
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: [action.executar_acao("Reiniciar", "Maquina",
                                                                                            maquina=entry2.get(),
                                                                                            tempo=entry3.get()),
                                                                       auto_restart(entry2.get(), 1, entry2.get(),
                                                                                    entry3.get()),
                                                                       screens.mostrar_comando_executado(
                                                                           janelaReiniciar,
                                                                           telaReiniciar)])

    # Reiniciar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_reiniciar_personalizado = customtkinter.CTkButton(janelaReiniciar, text="Reiniciar", width=170, height=50,
                                                            font=fonte,
                                                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                            command=lambda: [
                                                                action.executar_acao("Reiniciar", "Personalizado",
                                                                                     inicio=entry4.get(),
                                                                                     fim=entry5.get(),
                                                                                     passo=entry6.get(),
                                                                                     tempo=entry7.get()),
                                                                auto_restart(entry4.get(), entry6.get(), entry5.get(),
                                                                             entry7.get()),
                                                                screens.mostrar_comando_executado(
                                                                    janelaReiniciar,
                                                                    telaReiniciar)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 285, window=botao_reiniciar_lab_inteiro)
    canvas1.create_window(323, 319, window=botao_reiniciar_maquina)
    canvas1.create_window(525, 350, window=botao_reiniciar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaReiniciar,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaReiniciar.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaReiniciar.mainloop()


def telaLogarUsuario():
    """
    --> Funcao que exibe a tela coms os parâmetros para o bat de logon, com um usuario e uma senha personalizada
    """
    # Janela principal
    janelaLogarUsuario = customtkinter.CTk()

    janelaLogarUsuario.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaLogarUsuario, altura=450)

    # Título
    janelaLogarUsuario.title("AUTOLOGIN")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaLogarUsuario, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de fundo e do ícone de olho
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open(assets + "olhoFechado.png").resize((20, 20)))
    screens.background(canvas1)

    # Imagem AutoLOGIN
    login = ImageTk.PhotoImage(Image.open(assets + "autoLOGIN.png"))
    canvas1.create_image(328, 50, image=login)

    # Botao para Voltar a janela principal
    botao_voltar = customtkinter.CTkButton(
        janelaLogarUsuario,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaLogarUsuario.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Campos de Entrada para o Login Personalizado
    # Login
    canvas1.create_text(197, 94, text="Login:", fill="white", font=("Arial", 10, "bold"))
    entrada_login = customtkinter.CTkEntry(janelaLogarUsuario, placeholder_text="Insira o usuário...", width=300,
                                           fg_color="transparent")
    canvas1.create_window(325, 120, window=entrada_login)
    # Senha
    canvas1.create_text(197, 150, text="Senha:", fill="white", font=("Arial", 10, "bold"))
    entrada_senha = customtkinter.CTkEntry(janelaLogarUsuario, placeholder_text="Insira a senha...", show="*",
                                           width=300,
                                           fg_color="transparent", height=35)
    canvas1.create_window(325, 178, window=entrada_senha)

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Botão Mostrar/Ocultar Senha com Ícone
    botao_mostrar_senha_usuario = customtkinter.CTkButton(janelaLogarUsuario, image=imagem_olho_fechado, width=0,
                                                          height=0,
                                                          command=lambda: password.mostrarSenha(entrada_senha,
                                                                                                botao_mostrar_senha_usuario),
                                                          text="", hover_color=cor_input,
                                                          fg_color=cor_input)
    canvas1.create_window(455, 178, window=botao_mostrar_senha_usuario)  # Posição ao lado do campo de senha

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaLogarUsuario.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fontePequena,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaLogarUsuario, width=75, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fontePequena,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    # canvas1.create_window(120, 330, window=entry)
    canvas1.create_window(323, 300, window=entry2)
    # canvas1.create_window(323, 360, window=entry3)
    canvas1.create_window(525, 300, window=entry4)
    canvas1.create_window(525, 331, window=entry5)
    canvas1.create_window(525, 362, window=entry6)
    # canvas1.create_window(525, 390, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    # increase_button = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(168, 330, window=increase_button)
    # increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    # increase_button.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(72, 330, window=decrease_button)
    # decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    # decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(370, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(276, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Personalizado)
    # increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
    #                                                   fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(370, 360, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
    #                                                   fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(276, 360, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Logar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(572, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(478, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(572, 331, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(478, 331, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(572, 362, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
                                                      fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(478, 362, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    # increase_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▲", width=18, height=28,
    #                                                   fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(572, 390, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLogarUsuario, text="▼", width=18, height=28,
    #                                                   fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(478, 390, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Logar Lab
    canvas1.create_text(120, 245, text="Logar Lab", fill="white", font=("Arial", 12, "bold"))
    # canvas1.create_text(120, 300, text="Tempo (Segundos)", fill="white", font=("Arial", 10, "bold"))

    def tentar_logar_lab(tipo_log):
        """
        --> Funcao que tenta logar em uma categoria especifica ('Lab', 'Maquina' ou 'Personalizado')
        apenas se os campos de login e senha estiverem preenchidos.
        :param tipo_log: Tipo de categoria do comando
        """
        if password.verificar_campos_vazios(entrada_login.get(), entrada_senha.get()):
            if tipo_log.strip().title() == "Lab":
                action.executar_acao(
                    f'Logar Usuário "{entrada_login.get()}"',
                    "Lab",
                    tempo=entry.get(),
                    senha=entrada_senha.get()
                )
                auto_login(1,1,99, entrada_login.get(), entrada_senha.get())
            elif tipo_log.strip().title() == "Maquina":
                action.executar_acao(
                    f'Logar Usuário "{entrada_login.get()}"',
                    "Maquina",
                    maquina=entry2.get(),
                    tempo=entry3.get(),
                    senha=entrada_senha.get()
                )
                auto_login(entry2.get(), 1, entry2.get(), entrada_login.get(), entrada_senha.get())
            elif tipo_log.strip().title() == "Personalizado":
                action.executar_acao(
                    f'Logar Usuário "{entrada_login.get()}"',
                    "Personalizado",
                    inicio=entry4.get(),
                    fim=entry5.get(),
                    passo=entry6.get(),
                    tempo=entry7.get(),
                    senha=entrada_senha.get()
                )
                auto_login(entry4.get(), entry6.get(), entry5.get(), entrada_login.get(), entrada_senha.get())

            # Mostra a tela de comando executado apenas se todos os campos estão preenchidos
            screens.mostrar_comando_executado(janelaLogarUsuario, telaLogarUsuario)

    # Logar Lab Inteiro
    botao_logar_lab_inteiro = customtkinter.CTkButton(janelaLogarUsuario, text="Logar", width=120, height=30,
                                                      font=fontePequena, bg_color="transparent",
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: tentar_logar_lab("Lab"))
    # Logar Máquina
    canvas1.create_text(323, 245, text="Logar Máquina", fill="white", font=("Arial", 12, "bold"))
    canvas1.create_text(323, 270, text="N° da Máquina", fill="white", font=("Arial", 10, "bold"))
    # canvas1.create_text(323, 330, text="Tempo (Segundos)", fill="white", font=("Arial", 10, "bold"))

    botao_logar_maquina = customtkinter.CTkButton(janelaLogarUsuario, text="Logar", width=120, height=30,
                                                  font=fontePequena, bg_color="transparent",
                                                  fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                  command=lambda: tentar_logar_lab("Maquina"))

    # Logar Personalizado
    canvas1.create_text(525, 245, text="Personalizado", fill="white", font=("Arial", 12, "bold"))
    canvas1.create_text(525, 270, text="Início, Fim e Passo", fill="white", font=("Arial", 10, "bold"))
    # canvas1.create_text(525, 362, text="Tempo (Segundos)", fill="white", font=("Arial", 10, "bold"))

    # Botões
    botao_logar_personalizado = customtkinter.CTkButton(janelaLogarUsuario, text="Logar", width=120, height=30,
                                                        font=fontePequena, bg_color="transparent",
                                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                        command=lambda: tentar_logar_lab("Personalizado"))

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 280, window=botao_logar_lab_inteiro)
    canvas1.create_window(323, 340, window=botao_logar_maquina)
    canvas1.create_window(525, 402, window=botao_logar_personalizado)

    # Loop
    janelaLogarUsuario.mainloop()


def telaLimpar():
    """
    --> Função que exibe a tela com os parâmetros do bat rd com o caminho para o disco d: das máquinas
    """
    # Janela principal
    janelaLimpar = customtkinter.CTk()

    janelaLimpar.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaLimpar)

    # Título
    janelaLimpar.title("AUTORD")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaLimpar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem RD
    remove = ImageTk.PhotoImage(Image.open(assets + "autoRD.png"))
    canvas1.create_image(328, 50, image=remove)

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaLimpar.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaLimpar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    #canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    #canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 200, window=entry4)
    canvas1.create_window(525, 235, window=entry5)
    canvas1.create_window(525, 270, window=entry6)
    #canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    # increase_button = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(185, 235, window=increase_button)
    # increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    # increase_button.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(55, 235, window=decrease_button)
    # decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    # decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(388, 268, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(258, 268, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Limpar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 270, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 270, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(590, 300, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(460, 300, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Limpar Lab
    canvas1.create_text(120, 140, text="Limpar Lab", fill="white", font=("Arial", 16, "bold"))
    # canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                       font=fonte,
                                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                       command=lambda: [ auto_rd(1, 1, 99),
                                                           action.executar_acao("Limpar", "Lab", tempo=entry.get()),
                                                           screens.mostrar_comando_executado(janelaLimpar,
                                                                                             telaLimpar)])
    # Limpar Máquina
    canvas1.create_text(323, 140, text="Limpar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [ auto_rd(entry2.get(), 1, entry2.get()),
                                                       action.executar_acao("Limpar", "Maquina", maquina=entry2.get(),
                                                                            # tempo=entry3.get()
                                                                            ),
                                                       screens.mostrar_comando_executado(janelaLimpar,
                                                                                         telaLimpar)])

    # Limpar Personalizado
    canvas1.create_text(525, 140, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 170, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [ auto_rd(entry4.get(), entry6.get(), entry5.get()),
                                                             action.executar_acao("Limpar", "Personalizado",
                                                                                  inicio=entry4.get(), fim=entry5.get(),
                                                                                  passo=entry6.get(),
                                                                                  tempo=entry7.get()),
                                                             screens.mostrar_comando_executado(
                                                                 janelaLimpar,
                                                                 telaLimpar)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 185, window=botao_limpar_lab_inteiro)
    canvas1.create_window(323, 250, window=botao_limpar_maquina)
    canvas1.create_window(525, 320, window=botao_limpar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaLimpar,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaLimpar.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaLimpar.mainloop()


def telaCopiar():
    """
        --> Função que exibe a tela com os parâmetros para cópia de arquivo para o D: das máquinas
    """
    # Janela principal
    janelaCopiar = customtkinter.CTk()

    janelaCopiar.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaCopiar)

    # Título
    janelaCopiar.title("AUTOCOPY")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaCopiar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem Mensagem
    remove = ImageTk.PhotoImage(Image.open(assets + "autoCOPY.png"))
    canvas1.create_image(328, 50, image=remove)

    # canvas1.create_text(70, 135, text="Mensagem:", fill="white", font=("Arial", 10, "bold"))
    # entrada_mensagem = customtkinter.CTkTextbox(janelaCopiar, width=450, height=60,
    #                                             border_width=1, border_color=cor_input_numerico)
    # canvas1.create_window(336, 135, window=entrada_mensagem)


    file_path = customtkinter.CTkTextbox(janelaCopiar, width=500, height=40, font=fonteBotaoP,
                                                border_width=1, border_color=cor_input_numerico)
    file_button = customtkinter.CTkButton(janelaCopiar, text="📄", width=40, height=40,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [
                                                       file_path.configure(state=customtkinter.NORMAL),
                                                       file_path.delete("0.0", "end"),
                                                       file_path.insert("0.0", customtkinter.filedialog.askopenfilename().replace("/", "\\")),
                                                       file_path.configure(state=customtkinter.DISABLED)
                                                   ])
    file_path.configure(state=customtkinter.DISABLED)
    canvas1.create_window(70, 135, window=file_button)
    canvas1.create_window(350, 135, window=file_path)


    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaCopiar.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaCopiar, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    # canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 250, window=entry2)
    # canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 250, window=entry4)
    canvas1.create_window(525, 285, window=entry5)
    canvas1.create_window(525, 320, window=entry6)
    # canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    # increase_button = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(185, 235, window=increase_button)
    # increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    # increase_button.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(55, 235, window=decrease_button)
    # decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    # decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaCopiar, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(384, 250, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaCopiar, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(262, 250, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(388, 268, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(258, 268, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Limpar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaCopiar, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 250, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaCopiar, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 250, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaCopiar, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 285, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaCopiar, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 285, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaCopiar, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 320, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaCopiar, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 320, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(590, 300, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(460, 300, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Mensagem Lab
    canvas1.create_text(120, 190, text="Copiar Lab", fill="white", font=("Arial", 16, "bold"))
    # canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_enviar_lab_inteiro = customtkinter.CTkButton(janelaCopiar, text="Enviar", width=145, height=40,
                                                       font=fonte,
                                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                       command=lambda: [auto_copy(1, 1, 99, file_path.get("0.0", "end")),
                                                                        action.executar_acao("Enviar", "Lab",
                                                                                             tempo=entry.get()),
                                                                        screens.mostrar_comando_executado(janelaCopiar,
                                                                                                          telaCopiar)])
    # Mensagem Máquina
    canvas1.create_text(323, 190, text="Copiar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 220, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_enviar_maquina = customtkinter.CTkButton(janelaCopiar, text="Enviar", width=145, height=40,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [auto_copy(entry2.get(), 1, entry2.get(), file_path.get("0.0", "end")),
                                                                    action.executar_acao("Enviar", "Maquina",
                                                                                         maquina=entry2.get(),
                                                                                         # tempo=entry3.get()
                                                                                         ),
                                                                    screens.mostrar_comando_executado(janelaCopiar,
                                                                                                      telaCopiar)])

    # Mensagem Personalizado
    canvas1.create_text(525, 190, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 220, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_enviar_personalizado = customtkinter.CTkButton(janelaCopiar, text="Enviar", width=145, height=40,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [
                                                             auto_copy(entry4.get(), entry6.get(), entry5.get(), file_path.get("0.0", "end")),
                                                             action.executar_acao("Enviar", "Personalizado",
                                                                                  inicio=entry4.get(), fim=entry5.get(),
                                                                                  passo=entry6.get(),
                                                                                  tempo=entry7.get()),
                                                             screens.mostrar_comando_executado(
                                                                 janelaCopiar,
                                                                 telaCopiar)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 230, window=botao_enviar_lab_inteiro)
    canvas1.create_window(323, 295, window=botao_enviar_maquina)
    canvas1.create_window(525, 365, window=botao_enviar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaCopiar,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaCopiar.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaCopiar.mainloop()


def telaPON():
    """
    --> Função que exibe a tela com os parâmetros do bat PON para logar nas máquinas
    """
    # Janela principal
    janelaPON = customtkinter.CTk()

    janelaPON.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaPON)

    # Título
    janelaPON.title("AUTOPON")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaPON, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file=assets + "fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem RD
    pon = ImageTk.PhotoImage(Image.open(assets + "autoPON.png"))
    canvas1.create_image(328, 50, image=pon)

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaPON.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaPON, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 165, window=entry4)
    canvas1.create_window(525, 200, window=entry5)
    canvas1.create_window(525, 235, window=entry6)
    canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    increase_button = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(185, 235, window=increase_button)
    increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(55, 235, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 268, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 268, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Logar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 165, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 165, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    increase_button_machine = customtkinter.CTkButton(janelaPON, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPON, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Logar Lab
    canvas1.create_text(120, 170, text="Logar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Logar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                       font=fonte,
                                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                       command=lambda: [
                                                           action.executar_acao("Logar PON", "Lab", tempo=entry.get()),
                                                           screens.mostrar_comando_executado(janelaPON,
                                                                                             telaPON)])
    # Logar Máquina
    canvas1.create_text(323, 140, text="Logar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [action.executar_acao("Logar PON", "Maquina",
                                                                                         maquina=entry2.get(),
                                                                                         tempo=entry3.get()),
                                                                    screens.mostrar_comando_executado(janelaPON,
                                                                                                      telaPON)])

    # Logar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [
                                                             action.executar_acao("Logar PON", "Personalizado",
                                                                                  inicio=entry4.get(), fim=entry5.get(),
                                                                                  passo=entry6.get(),
                                                                                  tempo=entry7.get()),
                                                             screens.mostrar_comando_executado(janelaPON,
                                                                                               telaPON)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 285, window=botao_limpar_lab_inteiro)
    canvas1.create_window(323, 319, window=botao_limpar_maquina)
    canvas1.create_window(525, 350, window=botao_limpar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaPON,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaPON.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaPON.mainloop()


def telaPN():
    """
    --> Função que exibe a tela com os parâmetros do bat PN para logar nas máquinas
    """
    # Janela principal
    janelaPN = customtkinter.CTk()

    janelaPN.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaPN)

    # Título
    janelaPN.title("AUTOPN")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaPN, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem PN
    pon = ImageTk.PhotoImage(Image.open(assets + "autoPN.png"))
    canvas1.create_image(328, 50, image=pon)

    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaPN.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaPN, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 165, window=entry4)
    canvas1.create_window(525, 200, window=entry5)
    canvas1.create_window(525, 235, window=entry6)
    canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    increase_button = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(185, 235, window=increase_button)
    increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(55, 235, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 268, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 268, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Limpar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 165, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 165, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    increase_button_machine = customtkinter.CTkButton(janelaPN, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaPN, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Logar Lab
    canvas1.create_text(120, 170, text="Logar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Logar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                       font=fonte,
                                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                       command=lambda: [
                                                           action.executar_acao("Logar PN", "Lab", tempo=entry.get()),
                                                           screens.mostrar_comando_executado(janelaPN,
                                                                                             telaPN)])
    # Logar Máquina
    canvas1.create_text(323, 140, text="Logar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [
                                                       action.executar_acao("Logar PN", "Maquina", maquina=entry2.get(),
                                                                            tempo=entry3.get()),
                                                       screens.mostrar_comando_executado(janelaPN,
                                                                                         telaPN)])

    # Limpar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [
                                                             action.executar_acao("Logar PN", "Personalizado",
                                                                                  inicio=entry4.get(), fim=entry5.get(),
                                                                                  passo=entry6.get(),
                                                                                  tempo=entry7.get()),
                                                             screens.mostrar_comando_executado(janelaPN,
                                                                                               telaPN)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 285, window=botao_limpar_lab_inteiro)
    canvas1.create_window(323, 319, window=botao_limpar_maquina)
    canvas1.create_window(525, 350, window=botao_limpar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaPN,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaPN.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaPN.mainloop()


# Funções
def verificar_login():
    """
    --> Função chamada ao clicar no botão de "Entrar" para capturar e validar os dados de login (por enquanto, só está printando os valores)
    """
    global nome_usuario
    # Pegando os valores preenchidos
    nome_usuario = entrada_nome.get().strip().title()
    login_usuario = entrada_login.get().strip().lower()
    senha_usuario = entrada_senha.get().strip()
    senha_cmd_usuario = entrada_senha_cmd.get().strip()

    # Verificação se algum dos campos está vazio
    if not nome_usuario or not login_usuario or not senha_usuario or not senha_cmd_usuario:
        # Exibe uma mensagem de alerta
        messagebox.showwarning("CAMPOS VAZIOS", "Atenção! Todos os campos devem ser preenchidos.")
        return  # Retorna para não continuar o processo se os campos não estiverem preenchidos

    # Printando no Terminal
    # print(f"Nome: {nome_usuario}")
    # print(f"Login: {login_usuario}")
    # print(f"Senha: {senha_usuario}")
    # print(f"Senha CMD: {senha_cmd_usuario}")

    janela_login.destroy()  # Fecha a janela de login ao final, pra chamar a telaPrincipal
    tela_confirmacao(nome_usuario, login_usuario, senha_usuario, senha_cmd_usuario)


# Função para exibir a tela de confirmação
def tela_confirmacao(nome_usuario, login_usuario, senha_usuario, senha_cmd_usuario):
    """
    --> Funcao para criar e exibir a tela de confirmacao das credenciais do monitor.
    :param nome_usuario: Nome preenchido monitor
    :param login_usuario: User do monitor
    :param senha_usuario: Senha do monitor
    :param senha_cmd_usuario: Senha para o cmd personalizado do monitor
    Essa funcao possibilita que o monitor volte a tela de login para cadastrar suas
    credenciais novamente, desconsiderando as preenchidas anteriormente.
    """
    global nome_user, login_user, senha_user

    nome_user = nome_usuario
    login_user = login_usuario
    senha_user = senha_usuario

    janela_confirmacao = customtkinter.CTk()
    screens.centralizar(janela_confirmacao)

    janela_confirmacao.iconbitmap(assets + "fiap-ico.ico")
    janela_confirmacao.title("CONFIRMAÇÃO DE DADOS")

    canvas_confirmacao = Canvas(janela_confirmacao, width=655, height=400, bd=-1000)
    canvas_confirmacao.pack(fill="both", expand=True)

    screens.background(canvas_confirmacao, assets + "fundoFiap.png")

    # Texto de Confirmacao
    confirmar = ImageTk.PhotoImage(Image.open(assets + "confirmacao.png").resize((319, 44)))
    canvas_confirmacao.create_image(326, 110, image=confirmar)

    canvas_confirmacao.create_text(166, 155, text=f"Nome: {nome_usuario}", fill="white", font=("Arial", 18, "bold"),
                                   anchor="w")
    canvas_confirmacao.create_text(166, 187, text=f"Login: {login_usuario}", fill="white", font=("Arial", 18, "bold"),
                                   anchor="w")
    canvas_confirmacao.create_text(166, 219, text=f"Senha: {'*' * len(senha_usuario)}", fill="white",
                                   font=("Arial", 18, "bold"), anchor="w")
    canvas_confirmacao.create_text(166, 249, text=f"Senha CMD: {'*' * len(senha_cmd_usuario)}", fill="white",
                                   font=("Arial", 18, "bold"), anchor="w")

    botao_voltar = customtkinter.CTkButton(janela_confirmacao, text="Voltar", width=152, height=40, font=fonteBotao,
                                           fg_color=cor_voltar, hover_color=cor_voltar_escuro,
                                           command=lambda: [janela_confirmacao.destroy(), tela_login()])
    canvas_confirmacao.create_window(241, 300, window=botao_voltar)

    botao_confirmar = customtkinter.CTkButton(janela_confirmacao, text="Confirmar", width=154, height=40,
                                              font=fonteBotao,
                                              fg_color=cor_continuar, hover_color=cor_continuar_escuro,
                                              command=lambda: [janela_confirmacao.destroy(),
                                                               telaPrincipal(nome_usuario),
                                                               cadastrar_monitor(nome_usuario, login_usuario,
                                                                                 senha_usuario)])
    canvas_confirmacao.create_window(404, 300, window=botao_confirmar)

    janela_confirmacao.mainloop()


def tela_login():
    """
    --> Funcao para criar e exibir a tela de login.
    Chamada tanto no inicio quanto ao voltar da tela de confirmacao.
    """
    global janela_login, entrada_nome, entrada_login, entrada_senha, entrada_senha_cmd, botao_mostrar_senha_usuario, botao_mostrar_senha_cmd  # Variáveis globais para acessar em outros momentos

    # Janela de Login
    janela_login = customtkinter.CTk()

    janela_login.iconbitmap(assets + "fiap-ico.ico")
    janela_login.title("LOGIN")

    screens.centralizar(janela_login)

    # Canvas2 para posicionar os elementos
    canvas2 = Canvas(janela_login, width=655, height=400, bd=-1000)
    canvas2.pack(fill="both", expand=True)

    # Carregando imagens
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open(assets + "olhoFechado.png").resize((20, 20)))

    screens.background(canvas2, assets + "fiapFundoLogin.png")

    # Layout da Tela de Login
    canvas2.create_text(267, 38, text="Bem-vindo, ", fill="white", font=("Arial", 23, "bold"))
    canvas2.create_text(412, 38, text="Monitor!", fill=cor_fundo, font=("Arial", 23, "bold"))

    # Nome do Monitor
    canvas2.create_text(206, 72, text="Nome:", fill="white", font=("Arial", 14, "bold"))
    entrada_nome = customtkinter.CTkEntry(janela_login, placeholder_text="Insira seu nome...", width=300,
                                          fg_color="transparent")
    canvas2.create_window(325, 103, window=entrada_nome)

    # Login do Monitor
    canvas2.create_text(297, 137, text="Login de Usuário (Runas):", fill="white", font=("Arial", 14, "bold"))
    entrada_login = customtkinter.CTkEntry(janela_login, placeholder_text="Insira o seu usuário...", width=300,
                                           fg_color="transparent")
    canvas2.create_window(325, 170, window=entrada_login)

    # Senha do Monitor
    canvas2.create_text(300, 207, text="Senha do Monitor (Runas):", fill="white", font=("Arial", 14, "bold"))
    entrada_senha = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha...", show="*", width=300,
                                           fg_color="transparent", height=35)
    canvas2.create_window(325, 240, window=entrada_senha)

    # Botão Mostrar/Ocultar Senha com Ícone
    botao_mostrar_senha_usuario = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0,
                                                          command=lambda: password.mostrarSenha(entrada_senha,
                                                                                                botao_mostrar_senha_usuario),
                                                          text="", hover_color=cor_input,
                                                          fg_color=cor_input)
    canvas2.create_window(455, 240, window=botao_mostrar_senha_usuario)  # Posição ao lado do campo de senha

    # Senha para o CMD
    canvas2.create_text(265, 278, text="Senha para o CMD:", fill="white", font=("Arial", 14, "bold"))
    entrada_senha_cmd = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha para o CMD...",
                                               show="*", width=300, fg_color="transparent", height=35)
    canvas2.create_window(325, 310, window=entrada_senha_cmd)

    botao_mostrar_senha_cmd = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0,
                                                      command=lambda: password.mostrarSenha(entrada_senha_cmd,
                                                                                            botao_mostrar_senha_cmd),
                                                      text="", hover_color=cor_input,
                                                      fg_color=cor_input)
    canvas2.create_window(455, 310, window=botao_mostrar_senha_cmd)  # Posição ao lado do campo de senha

    # Botão Entrar
    botao_entrar = customtkinter.CTkButton(janela_login, text="Entrar", width=300, height=34, command=verificar_login,
                                           fg_color=cor_fundo, font=fonteBotao, hover_color=cor_fundo_escuro)
    canvas2.create_window(325, 355, window=botao_entrar)

    # Iniciar o loop da tela de login
    janela_login.mainloop()


def telaMensagem():
    """
        --> Função que exibe a tela com os parâmetros da mensagem a ser enviada para as máquinas
    """
    # Janela principal
    janelaMensagem = customtkinter.CTk()

    janelaMensagem.iconbitmap(assets + "fiap-ico.ico")

    screens.centralizar(janelaMensagem)

    # Título
    janelaMensagem.title("AUTOMESSAGE")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaMensagem, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    screens.background(canvas1)

    # Imagem Mensagem
    remove = ImageTk.PhotoImage(Image.open(assets + "autoMESSAGE.png"))
    canvas1.create_image(328, 50, image=remove)

    canvas1.create_text(70, 135, text="Mensagem:", fill="white", font=("Arial", 10, "bold"))
    entrada_mensagem = customtkinter.CTkTextbox(janelaMensagem, width=450, height=60,
                                                border_width=1, border_color=cor_input_numerico)
    canvas1.create_window(336, 135, window=entrada_mensagem)


    # Campos dos Inputs
    global entry, entry2, entry3, entry4, entry5, entry6, entry7
    vcmd = (janelaMensagem.register(validate_input), "%P")  # "%P" passa o valor atual para a função de validação
    entry = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                   font=fonte,
                                   validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry.insert(0, "5")  # Valor inicial
    entry2 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry2.insert(0, "1")  # Valor inicial
    entry3 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry3.insert(0, "5")  # Valor inicial
    entry4 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry4.insert(0, "1")  # Valor inicial
    entry5 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry5.insert(0, "40")  # Valor inicial
    entry6 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry6.insert(0, "1")  # Valor inicial
    entry7 = customtkinter.CTkEntry(janelaMensagem, width=100, justify="center", fg_color=cor_fundo_input_numerico,
                                    font=fonte,
                                    validate="key", validatecommand=vcmd, border_color=cor_fundo_input_numerico)
    entry7.insert(0, "5")  # Valor inicial

    # Inputs numéricos
    # canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 250, window=entry2)
    # canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 250, window=entry4)
    canvas1.create_window(525, 285, window=entry5)
    canvas1.create_window(525, 320, window=entry6)
    # canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    # increase_button = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(185, 235, window=increase_button)
    # increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    # increase_button.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                           hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                           border_width=-100)
    # canvas1.create_window(55, 235, window=decrease_button)
    # decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    # decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor (Máquina)
    increase_button_machine = customtkinter.CTkButton(janelaMensagem, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(384, 250, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry2))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaMensagem, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(262, 250, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry2))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de aumentar e diminuir o valor do tempo (Máquina)
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(388, 268, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(258, 268, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Limpar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaMensagem, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 250, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaMensagem, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 250, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaMensagem, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 285, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaMensagem, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 285, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaMensagem, text="▲", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(586, 320, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaMensagem, text="▼", width=18, height=28, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(464, 320, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    # increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(590, 300, window=increase_button_machine)
    # increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    # increase_button_machine.bind("<ButtonRelease-1>", stop_increment)
    #
    # decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
    #                                                   hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
    #                                                   border_width=-100)
    # canvas1.create_window(460, 300, window=decrease_button_machine)
    # decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    # decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Mensagem Lab
    canvas1.create_text(120, 190, text="Mensagem Lab", fill="white", font=("Arial", 16, "bold"))
    # canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_enviar_lab_inteiro = customtkinter.CTkButton(janelaMensagem, text="Enviar", width=145, height=40,
                                                       font=fonte,
                                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                       command=lambda: [auto_message(1, 1, 99, entrada_mensagem.get("0.0", "end")),
                                                                        action.executar_acao("Enviar", "Lab",
                                                                                             tempo=entry.get()),
                                                                        screens.mostrar_comando_executado(janelaMensagem,
                                                                                                          telaMensagem)])
    # Mensagem Máquina
    canvas1.create_text(323, 190, text="Mensagem Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 220, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_enviar_maquina = customtkinter.CTkButton(janelaMensagem, text="Enviar", width=145, height=40,
                                                   font=fonte,
                                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                   command=lambda: [auto_message(entry2.get(), 1, entry2.get(), entrada_mensagem.get("0.0", "end")),
                                                                    action.executar_acao("Enviar", "Maquina",
                                                                                         maquina=entry2.get(),
                                                                                         # tempo=entry3.get()
                                                                                         ),
                                                                    screens.mostrar_comando_executado(janelaMensagem,
                                                                                                      telaMensagem)])

    # Mensagem Personalizado
    canvas1.create_text(525, 190, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 220, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    # canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_enviar_personalizado = customtkinter.CTkButton(janelaMensagem, text="Enviar", width=145, height=40,
                                                         font=fonte,
                                                         fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                         command=lambda: [
                                                             auto_message(entry4.get(), entry6.get(), entry5.get(), entrada_mensagem.get("0.0", "end")),
                                                             action.executar_acao("Enviar", "Personalizado",
                                                                                  inicio=entry4.get(), fim=entry5.get(),
                                                                                  passo=entry6.get(),
                                                                                  tempo=entry7.get()),
                                                             screens.mostrar_comando_executado(
                                                                 janelaMensagem,
                                                                 telaMensagem)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 230, window=botao_enviar_lab_inteiro)
    canvas1.create_window(323, 295, window=botao_enviar_maquina)
    canvas1.create_window(525, 365, window=botao_enviar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaMensagem,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaMensagem.destroy(), telaPrincipal(nome_user)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaMensagem.mainloop()


checar_bitlocker()
