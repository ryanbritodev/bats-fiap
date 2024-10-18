import os
from tkinter import Canvas, PhotoImage, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

# Configurações iniciais
ctk.set_appearance_mode("dark")

# Dimensões da janela
altura = 400
largura = 655

# Definição de fontes e cores
fonte = ("Arial", 18, "bold")
fonteBotao = ("Arial", 16, "bold")
fonteBotaoP = ("Arial", 14, "bold")

cor_fundo = "#ed145b"
cor_fundo_escuro = "#d01150"
cor_input = "#242424"
cor_continuar = "#039A2B"
cor_continuar_escuro = "#027C23"
cor_voltar = "#D90404"
cor_voltar_escuro = "#BC0404"

# Variáveis globais para controle do estado dos botões
incrementing = False
decrementing = False


# Função para aumentar o valor
def increment():
    if incrementing:
        current_value = int(entry.get())
        entry.delete(0, ctk.END)
        entry.insert(0, str(current_value + 1))
        root.after(100, increment)


# Função para diminuir o valor
def decrement():
    if decrementing:
        current_value = int(entry.get())
        if current_value > 1:
            entry.delete(0, ctk.END)
            entry.insert(0, str(current_value - 1))
        else:
            messagebox.showerror("Erro", "O valor deve ser maior que 0.")
            entry.delete(0, ctk.END)
            entry.insert(0, "1")
        root.after(100, decrement)


# Funções para controlar incremento e decremento contínuos
def start_increment(event):
    global incrementing
    incrementing = True
    increment()


def stop_increment(event):
    global incrementing
    incrementing = False


def start_decrement(event):
    global decrementing
    decrementing = True
    decrement()


def stop_decrement(event):
    global decrementing
    decrementing = False


# Função para capturar o valor final
def enviar():
    valor_final = entry.get()
    print(f"Valor final escolhido: {valor_final}")


# Funções BATS
def executar_bat_desligar():
    os.system("shutdown.bat")


# Telas
def telaPrincipal(nome_usuario):
    """
    Função que exibe a tela principal após o login
    """
    janela = ctk.CTk()

    janela.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janela.winfo_screenheight()
    larguraTela = janela.winfo_screenwidth()

    # Calculando o eixo X e Y para centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janela.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
    janela.minsize(655, 400)
    janela.maxsize(655, 400)
    janela.title("FIAP AUTOLAB")

    # Canvas
    canvas1 = Canvas(janela, width=655, height=400, bd=-100)
    canvas1.pack(fill="both", expand=True)

    # Imagem de fundo
    imagemFundo = PhotoImage(file="../assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

    # Logo FIAP
    logoFiap = PhotoImage(file="../assets/fiapLogo.png")
    canvas1.create_image(330, 67, image=logoFiap)

    # Texto AUTOLAB
    autoLab = PhotoImage(file="../assets/autoLAB.png")
    canvas1.create_image(324, 116, image=autoLab)

    # Mensagem de boas-vindas personalizada
    canvas1.create_text(325, 180, text=f"Bem-vindo, {nome_usuario}!", fill="white", font=("Arial", 20, "bold"))

    # Botões de ação
    botao_desligar = ctk.CTkButton(janela, text="Desligar", width=130, height=40, font=fonteBotaoP,
                                   fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                   command=lambda: [janela.destroy(), telaDesligar()])

    botao_reiniciar = ctk.CTkButton(janela, text="Reiniciar", width=130, height=40, font=fonteBotaoP,
                                    fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    botao_limpar = ctk.CTkButton(janela, text="Limpar o (D:)", width=130, height=40, font=fonteBotaoP,
                                 fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    botao_logar = ctk.CTkButton(janela, text="Logar Usuário", width=130, height=40, font=fonteBotaoP,
                                fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Posicionando os botões no Canvas
    canvas1.create_window(118, 250, window=botao_desligar)
    canvas1.create_window(118, 300, window=botao_reiniciar)
    canvas1.create_window(118, 350, window=botao_logar)
    canvas1.create_window(258, 250, window=botao_limpar)

    janela.mainloop()


def telaDesligar():
    """
    Função que exibe a tela de shutdown
    """
    janelaDesligar = ctk.CTk()

    janelaDesligar.iconbitmap("./assets/fiap-ico.ico")
    alturaTela = janelaDesligar.winfo_screenheight()
    larguraTela = janelaDesligar.winfo_screenwidth()
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)
    janelaDesligar.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
    janelaDesligar.minsize(655, 400)
    janelaDesligar.maxsize(655, 400)
    janelaDesligar.title("AUTOSHUTDOWN")

    # Canvas e fundo
    canvas1 = Canvas(janelaDesligar, width=655, height=400, bd=-100)
    canvas1.pack(fill="both", expand=True)
    fundo = PhotoImage(file="../assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem Shutdown
    shutdown = PhotoImage(file="../assets/autoSHUTDOWN.png")
    canvas1.create_image(328, 70, image=shutdown)

    # Desligar Lab Inteiro
    canvas1.create_text(120, 185, text="Desligar Lab", fill="white", font=("Arial", 21, "bold"))
    botao_desligar_lab_inteiro = ctk.CTkButton(janelaDesligar, text="Desligar", width=170, height=50, font=fonte,
                                               fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Campo de entrada numérica
    global entry
    entry = ctk.CTkEntry(janelaDesligar, width=100, justify="center")
    entry.insert(0, "1")  # Valor inicial
    canvas1.create_window(328, 200, window=entry)

    # Botões de aumentar e diminuir o valor
    increase_button = ctk.CTkButton(janelaDesligar, text="▲", width=30)
    canvas1.create_window(380, 200, window=increase_button)
    increase_button.bind("<ButtonPress-1>", start_increment)
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = ctk.CTkButton(janelaDesligar, text="▼", width=30)
    canvas1.create_window(276, 200, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", start_decrement)
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Botão de enviar
    send_button = ctk.CTkButton(janelaDesligar, text="Enviar", command=enviar)
    canvas1.create_window(328, 260, window=send_button)

    janelaDesligar.mainloop()


# Função de login
def verificar_login():
    nome_usuario = entrada_nome.get().strip().title()
    login_usuario = entrada_login.get().strip().lower()
    senha_usuario = entrada_senha.get().strip()
    senha_cmd_usuario = entrada_senha_cmd.get().strip()

    if not nome_usuario or not login_usuario or not senha_usuario or not senha_cmd_usuario:
        messagebox.showwarning("Cuidado!", "Por favor, preencha todos os campos!")
    else:
        root.destroy()
        telaPrincipal(nome_usuario)


# Tela inicial de login
root = ctk.CTk()

root.iconbitmap("./assets/fiap-ico.ico")

alturaTela = root.winfo_screenheight()
larguraTela = root.winfo_screenwidth()

eixoX = (larguraTela / 2) - (largura / 2)
eixoY = (alturaTela / 2) - (altura / 2)

root.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
root.minsize(655, 400)
root.maxsize(655, 400)
root.title("FIAP AUTOLAB")

canvas = Canvas(root, width=655, height=400, bd=-100)
canvas.pack(fill="both", expand=True)

imagemFundo = PhotoImage(file="../assets/fundoFiap.png")
canvas.create_image(0, 0, image=imagemFundo, anchor="nw")

# Logotipo
imagemLogo = PhotoImage(file="../assets/fiapLogo.png")
canvas.create_image(325, 40, image=imagemLogo)

# Entradas de dados
canvas.create_text(325, 120, text="Nome:", fill="white", font=fonte)
entrada_nome = ctk.CTkEntry(root, width=200)
canvas.create_window(325, 150, window=entrada_nome)

canvas.create_text(325, 180, text="Login:", fill="white", font=fonte)
entrada_login = ctk.CTkEntry(root, width=200)
canvas.create_window(325, 210, window=entrada_login)

canvas.create_text(325, 240, text="Senha:", fill="white", font=fonte)
entrada_senha = ctk.CTkEntry(root, width=200, show="*")
canvas.create_window(325, 270, window=entrada_senha)

canvas.create_text(325, 300, text="Senha CMD:", fill="white", font=fonte)
entrada_senha_cmd = ctk.CTkEntry(root, width=200, show="*")
canvas.create_window(325, 330, window=entrada_senha_cmd)

# Botão de login
botao_login = ctk.CTkButton(root, text="Entrar", width=100, font=fonteBotaoP,
                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                            command=verificar_login)
canvas.create_window(325, 370, window=botao_login)

root.mainloop()
