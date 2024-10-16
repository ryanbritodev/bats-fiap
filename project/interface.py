# FIAP AUTOLAB
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
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")

altura = 400
largura = 655

# Fonte e Cores
fonte = ("Arial", 18, "bold")
fonteBotao = ("Arial", 16, "bold")
cor_fundo = "#ed145b"
cor_fundo_escuro = "#d01150"
cor_input = "#242424"


# BATS
def executar_bat_desligar():
    os.system("shutdown.bat")  # Substituir posteriormente pelos caminhos dos bats


# Telas
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

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janela.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janela.minsize(655, 400)
    janela.maxsize(655, 400)

    # Título
    janela.title("FIAP AUTOLAB")

    # Canvas1
    canvas1 = Canvas(janela, width=655, height=400)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    imagemFundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

    # Logo da FIAP
    logoFiap = PhotoImage(file="./assets/fiapLogo.png")
    canvas1.create_image(330, 67, image=logoFiap)

    # Texto AUTOLAB
    autoLab = PhotoImage(file="assets/autoLAB.png")
    canvas1.create_image(324, 116, image=autoLab)

    # Mensagem de boas-vindas personalizada
    canvas1.create_text(325, 180, text=f"Bem-vindo, {nome_usuario}!", fill="white", font=("Arial", 20, "bold"))

    # Botões no Canvas (sem o parâmetro "command" pra executar os bats, por enquanto)
    botao_desligar = customtkinter.CTkButton(janela, text="Desligar Lab", width=170, height=40, font=fonte,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_reiniciar = customtkinter.CTkButton(janela, text="Reiniciar Lab", width=170, height=40, font=fonte,
                                              fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(140, 230, window=botao_desligar)
    canvas1.create_window(140, 280, window=botao_reiniciar)

    # Loop da Janela principal
    janela.mainloop()


# Funções
def verificar_login():
    """
    --> Função chamada ao clicar no botão de "Entrar" para capturar e validar os dados de login (por enquanto, só está printando os valores)
    """
    # Pegando os valores preenchidos
    nome_usuario = entrada_nome.get().strip().title()
    login_usuario = entrada_login.get().strip().lower()
    senha_usuario = entrada_senha.get().strip()
    senha_cmd_usuario = entrada_senha_cmd.get().strip()

    # Printando no Terminal
    print(f"Nome: {nome_usuario}")
    print(f"Login: {login_usuario}")
    print(f"Senha: {senha_usuario}")
    print(f"Senha CMD: {senha_cmd_usuario}")

    janela_login.destroy()  # Fecha a janela de login ao final, pra chamar a telaPrincipal
    telaPrincipal(nome_usuario)  # Chama a função para mostrar a telaPrincipal com o nome do usuário


def mostrar_senha_usuario():
    """
    --> Função para mostrar e esconder a senha do monitor
    """
    if entrada_senha.cget('show') == '*':
        entrada_senha.configure(show='')  # Mostra a senha
        botao_mostrar_senha_usuario.configure(image=imagem_olho)  # Altera o ícone para uma imagem de um olho aberto
    else:
        entrada_senha.configure(show='*')  # Oculta a senha
        botao_mostrar_senha_usuario.configure(image=imagem_olho_fechado)  # Altera o ícone para uma imagem de um olho fechado


def mostrar_senha_cmd():
    """
    --> Mesma lógica da função mostrar_senha_usuario(), porém para mostrar e esconder a senha do campo do CMD
    """
    if entrada_senha_cmd.cget('show') == '*':
        entrada_senha_cmd.configure(show='')  # Mostra a senha
        botao_mostrar_senha_cmd.configure(image=imagem_olho)  # Altera o ícone para uma imagem de um olho aberto
    else:
        entrada_senha_cmd.configure(show='*')  # Oculta a senha
        botao_mostrar_senha_cmd.configure(image=imagem_olho_fechado)  # Altera o ícone para uma imagem de um olho fechado


# Janela de Login
janela_login = customtkinter.CTk()

janela_login.iconbitmap("./assets/fiap-ico.ico")
janela_login.minsize(400, 300)  # Tamanho mínimo pra janela
janela_login.title("LOGIN")

# Centralizar janela
alturaTela = janela_login.winfo_screenheight()
larguraTela = janela_login.winfo_screenwidth()

# Calculando o eixo X e Y para centralizar a janela
eixoX = (larguraTela / 2) - (largura / 2)
eixoY = (alturaTela / 2) - (altura / 2)

# Definindo o tamanho e a posição da janela
janela_login.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
janela_login.minsize(655, 400)
janela_login.maxsize(655, 400)

# Canvas
canvas2 = Canvas(janela_login, width=655, height=400)
canvas2.pack(fill="both", expand=True)

# Carregando imagens
imagem_olho = ImageTk.PhotoImage(Image.open("./assets/olho.png").resize((20, 20)))
imagem_olho_fechado = ImageTk.PhotoImage(Image.open("./assets/olhoFechado.png").resize((20, 20)))
imagemFundoLogin = PhotoImage(file="assets/fiapFundoLogin.png")
canvas2.create_image(0, 0, image=imagemFundoLogin, anchor="nw")

# Layout da Tela de Login
canvas2.create_text(267, 38, text="Bem-vindo, ", fill="white", font=("Arial", 23, "bold"))
canvas2.create_text(412, 38, text="Monitor!", fill=cor_fundo, font=("Arial", 23, "bold"))

# Nome do Monitor
canvas2.create_text(202, 72, text="Nome", fill="white", font=("Arial", 14, "bold"))
entrada_nome = customtkinter.CTkEntry(janela_login, placeholder_text="Insira seu nome...", width=300, fg_color="transparent")
canvas2.create_window(325, 103, window=entrada_nome)

# Login do Monitor
canvas2.create_text(293, 137, text="Login de Usuário (Runas)", fill="white", font=("Arial", 14, "bold"))
entrada_login = customtkinter.CTkEntry(janela_login, placeholder_text="Insira o seu usuário...", width=300, fg_color="transparent")
canvas2.create_window(325, 170, window=entrada_login)

# Senha do Monitor
canvas2.create_text(296, 207, text="Senha do Monitor (Runas)", fill="white", font=("Arial", 14, "bold"))
entrada_senha = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha...", show="*", width=300, fg_color="transparent", height=35)
canvas2.create_window(325, 240, window=entrada_senha)

# Botão Mostrar/Ocultar Senha com Ícone
botao_mostrar_senha_usuario = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0, command=mostrar_senha_usuario, text="", hover_color=cor_input, fg_color=cor_input)
canvas2.create_window(455, 240, window=botao_mostrar_senha_usuario)  # Posição ao lado do campo de senha

# Senha para o CMD
canvas2.create_text(265, 278, text="Senha para o CMD:", fill="white", font=("Arial", 14, "bold"))
entrada_senha_cmd = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha para o CMD...", show="*", width=300, fg_color="transparent", height=35)
canvas2.create_window(325, 310, window=entrada_senha_cmd)

botao_mostrar_senha_cmd = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0, command=mostrar_senha_cmd, text="", hover_color=cor_input, fg_color=cor_input)
canvas2.create_window(455, 310, window=botao_mostrar_senha_cmd)  # Posição ao lado do campo de senha

# Botão Entrar
botao_entrar = customtkinter.CTkButton(janela_login, text="Entrar", width=300, height=34, command=verificar_login, fg_color=cor_fundo, font=fonteBotao, hover_color=cor_fundo_escuro)
canvas2.create_window(325, 355, window=botao_entrar)

# Iniciar o loop da tela de login
janela_login.mainloop()
