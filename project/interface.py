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
customtkinter.set_default_color_theme("blue")


def center(win):
    """
    --> Função que centraliza uma janela do Tkinter
    :param win: A janela principal que você deseja centralizar
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def executar_comando_desligar():
    os.system("shutdown.bat")  # Substituir posteriormente pelos caminhos dos bats


# Login
usuario_nome = "Ryan"  # Pensei de fazermos uma tela de login, pra primeira vez que o usuário entrar, onde ele vai definir o nome, a senha pro cmd e a senha e o usuário do runas

# Janela principal
janela = customtkinter.CTk()

janela.iconbitmap("./assets/fiap-ico.ico")

# Tamanho da Janela
janela.geometry("626x391")
janela.minsize(626, 391)  # Garantir tamanho mínimo da janela

# Título
janela.title("FIAP Autobats")

# Centralizar a janela
center(janela)

# Canvas
canvas1 = Canvas(janela, width=600, height=600)
canvas1.pack(fill="both", expand=True)

# Carregar e exibir imagem de fundo
imagemFundo = PhotoImage(file="./assets/fundoFiap.png")
canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

# Logo da FIAP
logoFiap = PhotoImage(file="./assets/fiapLogo.png")
canvas1.create_image(400, 100, image=logoFiap)

# Cores dos Botões
cor_fundo = "#e4336c"
cor_fundo_escuro = "#c62c5c"

# Fonte
fonte = ("Arial", 18, "bold")

# Mensagem de boas-vindas personalizada
canvas1.create_text(355, 165, text=f"Bem-vindo,", fill="white", font=("Arial", 20, "bold"))
canvas1.create_text(475, 165, text=f"{usuario_nome}!", fill=cor_fundo, font=("Arial", 20, "bold"))

# Botões no Canvas (sem command, por enquanto)
botao_desligar = customtkinter.CTkButton(janela, text="Desligar Lab", width=170, height=40, font=fonte, fg_color=cor_fundo, hover_color=cor_fundo_escuro)

# Posicionando os botões sobre o Canvas
canvas1.create_window(400, 350, window=botao_desligar)

# Iniciando o loop da interface
janela.mainloop()
