# INTERFACE GRÁFICA AUTOBATS
# IMPORTANTE: se você achou este pen drive, NÃO EXECUTE OS COMANDOS, eles servem
# única e exclusivamente para auxílio de monitores, utilizá-los indevidamente pode acarretar
# em problemas sérios.
# Créditos:
# Victor Flávio Demarchi Viana
# Ryan Brito Pereira Ramos

import os
from tkinter import Canvas
from tkinter import PhotoImage
import customtkinter

customtkinter.set_appearance_mode("dark")

altura = 400
largura = 655

# BATS
def executar_bat_desligar():
    os.system("shutdown.bat")  # Substituir posteriormente pelos caminhos dos bats


# TELAS
def telaPrincipal(nome_usuario):
    """
    --> Função que exibe a tela principal após o login
    :param nome_usuario: Nome do usuário preenchido na tela de login
    """
    # Janela principal
    janela = customtkinter.CTk()

    janela.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janela.winfo_screenheight()
    larguraTela = janela.winfo_screenwidth()

    # Calculando o eixo X e Y para centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janela.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janela.minsize(655, 400)
    janela.maxsize(655, 400)

    # Título
    janela.title("FIAP AutoLab")

    # Canvas
    canvas1 = Canvas(janela, width=655, height=400)
    canvas1.pack(fill="both", expand=True)

    # Carregar e exibir imagem de fundo
    imagemFundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

    # Logo da FIAP
    logoFiap = PhotoImage(file="./assets/fiapLogo.png")
    canvas1.create_image(410, 67, image=logoFiap)

    # AutoLab
    autoLab = PhotoImage(file="./assets/autoLAB.png")
    canvas1.create_image(400, 135, image=autoLab)

    # Cores dos Botões
    cor_fundo = "#ed145b"
    cor_fundo_escuro = "#d01150"

    # Fonte
    fonte = ("Arial", 18, "bold")

    # Mensagem de boas-vindas personalizada
    canvas1.create_text(362, 200, text=f"Bem-vindo,", fill="white", font=("Arial", 20, "bold"))
    canvas1.create_text(482, 200, text=f"{nome_usuario}!", fill=cor_fundo, font=("Arial", 20, "bold"))

    # Botões no Canvas (sem command, por enquanto)
    botao_desligar = customtkinter.CTkButton(janela, text="Desligar Lab", width=170, height=40, font=fonte,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_reiniciar = customtkinter.CTkButton(janela, text="Reiniciar Lab", width=170, height=40, font=fonte,
                                              fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(165, 290, window=botao_desligar)
    canvas1.create_window(165, 360, window=botao_reiniciar)

    # Loop da Janela principal
    janela.mainloop()


# Função para exibir os dados coletados pelo usuário da tela de login
def verificar_login():
    """
    --> Função chamada ao clicar no botão de "Entrar" para capturar e validar os dados de login
    :return: Não possui retorno
    """
    nome_usuario = entrada_nome.get().strip().title()  # Pega o nome do campo de entrada
    login_usuario = entrada_login.get()
    senha_usuario = entrada_senha.get()

    # Para este exemplo, vamos apenas imprimir as informações no terminal
    print(f"Nome: {nome_usuario}")
    print(f"Login: {login_usuario}")
    print(f"Senha: {senha_usuario}")

    janela_login.destroy()  # Fecha a janela de login
    telaPrincipal(nome_usuario)  # Chama a função para mostrar a tela principal com o nome do usuário


# Janela de Login
janela_login = customtkinter.CTk()

janela_login.iconbitmap("./assets/fiap-ico.ico")
janela_login.geometry("400x300")
janela_login.minsize(400, 300)  # Garantir tamanho mínimo da janela
janela_login.title("Login Autobats")

# Centralizar janela
alturaTela = janela_login.winfo_screenheight()
larguraTela = janela_login.winfo_screenwidth()

# Calculando o eixo X e Y para centralizar a janela
eixoX = (larguraTela / 2) - (largura / 2)
eixoY = (alturaTela / 2) - (altura / 2)

# Definindo o tamanho e a posição da janela
janela_login.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

# Layout da Tela de Login
label_bemvindo = customtkinter.CTkLabel(janela_login, text="Bem-vindo! Por favor, faça o login.", font=("Arial", 18, "bold"))
label_bemvindo.pack(pady=10)

# Campo Nome
entrada_nome = customtkinter.CTkEntry(janela_login, placeholder_text="Nome", width=200)
entrada_nome.pack(pady=10)

# Campo Login de Usuário (Runas)
entrada_login = customtkinter.CTkEntry(janela_login, placeholder_text="Login de Usuário (Runas)", width=200)
entrada_login.pack(pady=10)

# Campo Senha de Usuário (Runas)
entrada_senha = customtkinter.CTkEntry(janela_login, placeholder_text="Senha de Usuário (Runas)", show="*", width=200)
entrada_senha.pack(pady=10)

# Botão Entrar
botao_entrar = customtkinter.CTkButton(janela_login, text="Entrar", width=150, command=verificar_login)
botao_entrar.pack(pady=20)

# Iniciar o loop da tela de login
janela_login.mainloop()
