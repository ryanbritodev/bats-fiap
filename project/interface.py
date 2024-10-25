# FIAP AUTOLAB
# IMPORTANTE: se você achou este pen drive, NÃO EXECUTE OS COMANDOS, eles servem
# única e exclusivamente para auxílio de monitores, utilizá-los indevidamente pode acarretar
# em problemas sérios.
# Créditos:
# Victor Flávio Demarchi Viana
# Ryan Brito Pereira Ramos

# Bibliotecas
import os
from tkinter import Canvas, PhotoImage, messagebox
import customtkinter
from PIL import Image, ImageTk
import ctypes

# Ícone da barra de tarefas da aplicação (Windows)
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Tema
customtkinter.set_appearance_mode("dark")

# Altura e Largura da Janela
altura = 400
largura = 655

# Fontes e Cores
fonte = ("Arial", 18, "bold")
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

# Variáveis globais para controle do estado dos botões
incrementing = False
decrementing = False


# Função para voltar à janela anterior, mostrando que o comando foi executado com sucesso
def mostrar_comando_executado(janela_anterior, tela_destino):
    """
    --> Função que exibe a mensagem de "Comando executado com sucesso!" com um botão de "Continuar"
    :param janela_anterior: Janela anterior que você deseja fechar
    :param tela_destino: Função que abre a próxima tela (por exemplo, telaPrincipal, telaReiniciar, etc.)
    """
    # Fechando a janela anterior
    janela_anterior.destroy()

    # Criando a nova janela de sucesso
    janela_sucesso = customtkinter.CTk()

    janela_sucesso.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janela_sucesso.winfo_screenheight()
    larguraTela = janela_sucesso.winfo_screenwidth()

    # Definindo tamanho e posição da janela
    largura, altura = 655, 400
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)
    janela_sucesso.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")

    # Tamanhos (Máximo e Mínimo)
    janela_sucesso.minsize(655, 400)
    janela_sucesso.maxsize(655, 400)

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janela_sucesso, width=655, height=400, bd=-100000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    imagemFundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

    # Título da janela
    janela_sucesso.title("SUCESSO")

    # Mensagem
    canvas1.create_text(325, 125, text="Comando Executado", fill="white", font=("Arial", 30, "bold"))
    canvas1.create_text(325, 167, text="com Sucesso!", fill=cor_fundo, font=("Arial", 30, "bold"))

    # Botão "Continuar"
    botao_continuar = customtkinter.CTkButton(
        janela_sucesso,
        text="Continuar",
        width=275,
        height=80,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        font=("Arial", 26, "bold"),
        command=lambda: [janela_sucesso.destroy(), tela_destino()]  # Chama a tela de destino passada como argumento
    )
    canvas1.create_window(325, 260, window=botao_continuar)

    # Exibindo a janela de sucesso
    janela_sucesso.mainloop()


# Função genérica para aumentar o valor de qualquer campo
def increment_value(entry_widget):
    if incrementing:
        current_value = int(entry_widget.get())
        entry_widget.delete(0, customtkinter.END)
        entry_widget.insert(0, str(current_value + 1))
        janela.after(100, lambda: increment_value(entry_widget))


# Função genérica para diminuir o valor de qualquer campo
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


# Funções para Desligar (Lab, Máquina e Personalizado)
def desligar():
    valor_final = entry.get()
    if valor_final == "" or not valor_final.isdigit() or valor_final == "0":  # Se o campo estiver vazio ou não for um número
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Desligar Lab: {valor_final}s")


def desligarMaquina():
    maquina = entry2.get()
    tempo = entry3.get()
    if maquina == "" or not maquina.isdigit() or maquina == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Máquina: {maquina}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Desligar: {tempo}s")


def desligarPersonalizado():
    inicio = entry4.get()
    fim = entry5.get()
    passo = entry6.get()
    tempo = entry7.get()
    if inicio == "" or not inicio.isdigit() or inicio == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Início: {inicio}")
    if fim == "" or not fim.isdigit() or fim == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Fim: {fim}")
    if passo == "" or not passo.isdigit() or passo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Passo: {passo}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Desligar: {tempo}s")


# Funções para Reiniciar (Lab, Máquina e Personalizado)
def reiniciar():
    valor_final = entry.get()
    if valor_final == "" or not valor_final.isdigit() or valor_final == "0":  # Se o campo estiver vazio ou não for um número
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Reiniciar Lab: {valor_final}s")


def reiniciarMaquina():
    maquina = entry2.get()
    tempo = entry3.get()
    if maquina == "" or not maquina.isdigit() or maquina == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Máquina: {maquina}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Reiniciar: {tempo}s")


def reiniciarPersonalizado():
    inicio = entry4.get()
    fim = entry5.get()
    passo = entry6.get()
    tempo = entry7.get()
    if inicio == "" or not inicio.isdigit() or inicio == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Início: {inicio}")
    if fim == "" or not fim.isdigit() or fim == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Fim: {fim}")
    if passo == "" or not passo.isdigit() or passo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Passo: {passo}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Reiniciar: {tempo}s")


# Funções para Limpar (Lab, Máquina e Personalizado)
def limpar():
    valor_final = entry.get()
    if valor_final == "" or not valor_final.isdigit() or valor_final == "0":  # Se o campo estiver vazio ou não for um número
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Limpar Lab: {valor_final}s")


def limparMaquina():
    maquina = entry2.get()
    tempo = entry3.get()
    if maquina == "" or not maquina.isdigit() or maquina == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Máquina: {maquina}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Limpar: {tempo}s")


def limparPersonalizado():
    inicio = entry4.get()
    fim = entry5.get()
    passo = entry6.get()
    tempo = entry7.get()
    if inicio == "" or not inicio.isdigit() or inicio == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Início: {inicio}")
    if fim == "" or not fim.isdigit() or fim == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Fim: {fim}")
    if passo == "" or not passo.isdigit() or passo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Passo: {passo}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Limpar: {tempo}s")


# Funções para logar PON (Lab, Máquina e Personalizado)
def logarPON():
    valor_final = entry.get()
    if valor_final == "" or not valor_final.isdigit() or valor_final == "0":  # Se o campo estiver vazio ou não for um número
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para logar PON no Lab: {valor_final}s")


def logarPONMaquina():
    maquina = entry2.get()
    tempo = entry3.get()
    if maquina == "" or not maquina.isdigit() or maquina == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Máquina: {maquina}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Logar PON: {tempo}s")


def logarPONPersonalizado():
    inicio = entry4.get()
    fim = entry5.get()
    passo = entry6.get()
    tempo = entry7.get()
    if inicio == "" or not inicio.isdigit() or inicio == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Início: {inicio}")
    if fim == "" or not fim.isdigit() or fim == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Fim: {fim}")
    if passo == "" or not passo.isdigit() or passo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Passo: {passo}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Logar PON: {tempo}s")


# Funções para logar PN (Lab, Máquina e Personalizado)
def logarPN():
    valor_final = entry.get()
    if valor_final == "" or not valor_final.isdigit() or valor_final == "0":  # Se o campo estiver vazio ou não for um número
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para logar PN no Lab: {valor_final}s")


def logarPNMaquina():
    maquina = entry2.get()
    tempo = entry3.get()
    if maquina == "" or not maquina.isdigit() or maquina == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Máquina: {maquina}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Logar PN: {tempo}s")


def logarPNPersonalizado():
    inicio = entry4.get()
    fim = entry5.get()
    passo = entry6.get()
    tempo = entry7.get()
    if inicio == "" or not inicio.isdigit() or inicio == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Início: {inicio}")
    if fim == "" or not fim.isdigit() or fim == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Fim: {fim}")
    if passo == "" or not passo.isdigit() or passo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Passo: {passo}")
    if tempo == "" or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido!")
    else:
        print(f"Tempo para Logar PN: {tempo}s")


# Função para validar a entrada (apenas números)
def validate_input(value):
    # Verifica se a entrada é um número ou vazia
    if value.isdigit() or value == "":
        return True
    else:
        return False


# Bats (Funções com a execução dos Bats)
def executar_bat_desligar():
    os.system("shutdown.bat")  # Substituir posteriormente pelos caminhos dos Bats


# Telas
def telaPrincipal(nome_usuario):
    """
    --> Função que exibe a tela principal após o login
    :param nome_usuario: Nome do usuário preenchido na tela de login
    """
    # Janela principal
    global janela
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

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janela, width=655, height=400, bd=-100000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    imagemFundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

    # Logo da FIAP
    logoFiap = PhotoImage(file="./assets/fiapLogo.png")
    canvas1.create_image(330, 62, image=logoFiap)

    # Texto AUTOLAB
    autoLab = PhotoImage(file="assets/autoLAB.png")
    canvas1.create_image(324, 111, image=autoLab)

    # Mensagem de boas-vindas personalizada
    canvas1.create_text(325, 175, text=f"Bem-vindo, {nome_usuario}!", fill="white", font=("Arial", 20, "bold"))

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
                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_pon = customtkinter.CTkButton(janela, text="Logar PON", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                        command=lambda: [janela.destroy(), telaPON()])
    botao_pn = customtkinter.CTkButton(janela, text="Logar PN", width=130, height=40, font=fonteBotaoP,
                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                       command=lambda: [janela.destroy(), telaPN()])
    botao_nac = customtkinter.CTkButton(janela, text="Abrir NAC", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_mensagem = customtkinter.CTkButton(janela, text="Mensagem", width=130, height=40, font=fonteBotaoP,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_logar = customtkinter.CTkButton(janela, text="Logar Usuário", width=130, height=40, font=fonteBotaoP,
                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_url = customtkinter.CTkButton(janela, text="Abrir URL", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)

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

    # Loop da Janela principal
    janela.mainloop()


def telaDesligar():
    """
    --> Função que exibe a tela com os parâmetros do bat shutdown
    """
    # Janela principal
    janelaDesligar = customtkinter.CTk()

    janelaDesligar.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janelaDesligar.winfo_screenheight()
    larguraTela = janelaDesligar.winfo_screenwidth()

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janelaDesligar.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janelaDesligar.minsize(655, 400)
    janelaDesligar.maxsize(655, 400)

    # Título
    janelaDesligar.title("AUTOSHUTDOWN")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaDesligar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem Shutdown
    shutdown = PhotoImage(file="assets/autoSHUTDOWN.png")
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
                                                         command=lambda: [desligar(),
                                                                          mostrar_comando_executado(janelaDesligar,
                                                                                                    telaDesligar)])
    # Desligar Máquina
    canvas1.create_text(323, 140, text="Desligar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_desligar_maquina = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50, font=fonte,
                                                     fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                     command=lambda: [desligarMaquina(),
                                                                      mostrar_comando_executado(janelaDesligar,
                                                                                                telaDesligar)])

    # Desligar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_desligar_personalizado = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50,
                                                           font=fonte,
                                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                           command=lambda: [desligarPersonalizado(),
                                                                            mostrar_comando_executado(janelaDesligar,
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
        command=lambda: [janelaDesligar.destroy(), telaPrincipal(nome_usuario)]
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

    janelaReiniciar.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janelaReiniciar.winfo_screenheight()
    larguraTela = janelaReiniciar.winfo_screenwidth()

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janelaReiniciar.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janelaReiniciar.minsize(655, 400)
    janelaReiniciar.maxsize(655, 400)

    # Título
    janelaReiniciar.title("AUTORESTART")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaReiniciar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem Shutdown
    restart = ImageTk.PhotoImage(Image.open("./assets/autoRESTART.png").resize((450, 225)))
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
                                                          command=lambda: [reiniciar(),
                                                                           mostrar_comando_executado(janelaReiniciar,
                                                                                                     telaReiniciar)])
    # Reiniciar Máquina
    canvas1.create_text(323, 140, text="Reiniciar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_reiniciar_maquina = customtkinter.CTkButton(janelaReiniciar, text="Reiniciar", width=170, height=50,
                                                      font=fonte,
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: [reiniciarMaquina(),
                                                                       mostrar_comando_executado(janelaReiniciar,
                                                                                                 telaReiniciar)])

    # ReiniciarReiniciar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_reiniciar_personalizado = customtkinter.CTkButton(janelaReiniciar, text="Reiniciar", width=170, height=50,
                                                            font=fonte,
                                                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                            command=lambda: [reiniciarPersonalizado(),
                                                                             mostrar_comando_executado(janelaReiniciar,
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
        command=lambda: [janelaReiniciar.destroy(), telaPrincipal(nome_usuario)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaReiniciar.mainloop()


def telaLimpar():
    """
    --> Função que exibe a tela com os parâmetros do bat rd com o caminho para o disco d: das máquinas
    """
    # Janela principal
    janelaLimpar = customtkinter.CTk()

    janelaLimpar.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janelaLimpar.winfo_screenheight()
    larguraTela = janelaLimpar.winfo_screenwidth()

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janelaLimpar.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janelaLimpar.minsize(655, 400)
    janelaLimpar.maxsize(655, 400)

    # Título
    janelaLimpar.title("AUTORD")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaLimpar, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem RD
    remove = ImageTk.PhotoImage(Image.open("./assets/autoRD.png").resize((450, 225)))
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
    canvas1.create_window(120, 235, window=entry)
    canvas1.create_window(323, 200, window=entry2)
    canvas1.create_window(323, 268, window=entry3)
    canvas1.create_window(525, 165, window=entry4)
    canvas1.create_window(525, 200, window=entry5)
    canvas1.create_window(525, 235, window=entry6)
    canvas1.create_window(525, 300, window=entry7)

    # Botões de aumentar e diminuir o valor (Lab)
    increase_button = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(185, 235, window=increase_button)
    increase_button.bind("<ButtonPress-1>", lambda event: start_increment(event, entry))
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                              hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                              border_width=-100)
    canvas1.create_window(55, 235, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry))
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

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
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(388, 268, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry3))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(258, 268, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry3))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Botões de Limpar Personalizado
    # Início
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 165, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry4))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 165, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry4))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Fim
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 200, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry5))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 200, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry5))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Passo
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 235, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry6))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 235, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry6))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Tempo
    increase_button_machine = customtkinter.CTkButton(janelaLimpar, text="▲", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(590, 300, window=increase_button_machine)
    increase_button_machine.bind("<ButtonPress-1>", lambda event: start_increment(event, entry7))
    increase_button_machine.bind("<ButtonRelease-1>", stop_increment)

    decrease_button_machine = customtkinter.CTkButton(janelaLimpar, text="▼", width=37, fg_color=cor_fundo,
                                                      hover_color=cor_fundo_escuro, border_color=cor_input_numerico,
                                                      border_width=-100)
    canvas1.create_window(460, 300, window=decrease_button_machine)
    decrease_button_machine.bind("<ButtonPress-1>", lambda event: start_decrement(event, entry7))
    decrease_button_machine.bind("<ButtonRelease-1>", stop_decrement)

    # Limpar Lab
    canvas1.create_text(120, 170, text="Limpar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                          font=fonte,
                                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                          command=lambda: [limpar(),
                                                                           mostrar_comando_executado(janelaLimpar,
                                                                                                     telaLimpar)])
    # Limpar Máquina
    canvas1.create_text(323, 140, text="Limpar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                      font=fonte,
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: [limparMaquina(),
                                                                       mostrar_comando_executado(janelaLimpar,
                                                                                                 telaLimpar)])

    # Limpar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaLimpar, text="Limpar", width=170, height=50,
                                                            font=fonte,
                                                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                            command=lambda: [limparPersonalizado(),
                                                                             mostrar_comando_executado(janelaLimpar,
                                                                                                       telaLimpar)])

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 285, window=botao_limpar_lab_inteiro)
    canvas1.create_window(323, 319, window=botao_limpar_maquina)
    canvas1.create_window(525, 350, window=botao_limpar_personalizado)

    botao_voltar = customtkinter.CTkButton(
        janelaLimpar,
        text="⬅",
        width=40,
        height=40,
        border_width=-1000,
        font=fonteBotaoP,
        fg_color=cor_fundo,
        hover_color=cor_fundo_escuro,
        command=lambda: [janelaLimpar.destroy(), telaPrincipal(nome_usuario)]
        # Fecha a tela atual e volta à principal
    )

    # Posicionando o botão de Voltar na tela
    canvas1.create_window(50, 48, window=botao_voltar)

    # Loop da Janela principal
    janelaLimpar.mainloop()


def telaPON():
    """
    --> Função que exibe a tela com os parâmetros do bat PON para logar nas máquinas
    """
    # Janela principal
    janelaPON = customtkinter.CTk()

    janelaPON.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janelaPON.winfo_screenheight()
    larguraTela = janelaPON.winfo_screenwidth()

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janelaPON.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janelaPON.minsize(655, 400)
    janelaPON.maxsize(655, 400)

    # Título
    janelaPON.title("AUTOPON")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaPON, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem RD
    pon = ImageTk.PhotoImage(Image.open("./assets/autoPON.png").resize((450, 225)))
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

    # Botões de Limpar Personalizado
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

    # Limpar Lab
    canvas1.create_text(120, 170, text="Logar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                          font=fonte,
                                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                          command=lambda: [logarPON(),
                                                                           mostrar_comando_executado(janelaPON,
                                                                                                     telaPON)])
    # Limpar Máquina
    canvas1.create_text(323, 140, text="Logar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                      font=fonte,
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: [logarPONMaquina(),
                                                                       mostrar_comando_executado(janelaPON,
                                                                                                 telaPON)])

    # Limpar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaPON, text="Logar", width=170, height=50,
                                                            font=fonte,
                                                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                            command=lambda: [logarPONPersonalizado(),
                                                                             mostrar_comando_executado(janelaPON,
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
        command=lambda: [janelaPON.destroy(), telaPrincipal(nome_usuario)]
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

    janelaPN.iconbitmap("./assets/fiap-ico.ico")

    # Pegando a altura e largura da tela
    alturaTela = janelaPN.winfo_screenheight()
    larguraTela = janelaPN.winfo_screenwidth()

    # Calculando o eixo X e Y pra centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janelaPN.geometry("{}x{}+{}+{}".format(largura, altura, int(eixoX), int(eixoY)))

    # Tamanhos (Máximo e Mínimo)
    janelaPN.minsize(655, 400)
    janelaPN.maxsize(655, 400)

    # Título
    janelaPN.title("AUTOPN")

    # Canvas1 para disposição dos elementos
    canvas1 = Canvas(janelaPN, width=655, height=400, bd=-1000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem RD
    pon = ImageTk.PhotoImage(Image.open("./assets/autoPON.png").resize((450, 225)))
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

    # Limpar Lab
    canvas1.create_text(120, 170, text="Logar Lab", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(120, 200, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Limpar Lab Inteiro
    botao_limpar_lab_inteiro = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                          font=fonte,
                                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                          command=lambda: [logarPN(),
                                                                           mostrar_comando_executado(janelaPN,
                                                                                                     telaPN)])
    # Limpar Máquina
    canvas1.create_text(323, 140, text="Logar Máquina", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(323, 170, text="N° da Máquina", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(323, 235, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    botao_limpar_maquina = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                      font=fonte,
                                                      fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                      command=lambda: [logarPNMaquina(),
                                                                       mostrar_comando_executado(janelaPN,
                                                                                                 telaPN)])

    # Limpar Personalizado
    canvas1.create_text(525, 105, text="Personalizado", fill="white", font=("Arial", 16, "bold"))
    canvas1.create_text(525, 133, text="Início, Fim e Passo", fill="white", font=("Arial", 14, "bold"))
    canvas1.create_text(525, 267, text="Tempo (Segundos)", fill="white", font=("Arial", 14, "bold"))

    # Botões
    botao_limpar_personalizado = customtkinter.CTkButton(janelaPN, text="Logar", width=170, height=50,
                                                            font=fonte,
                                                            fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                                            command=lambda: [logarPNPersonalizado(),
                                                                             mostrar_comando_executado(janelaPN,
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
        command=lambda: [janelaPN.destroy(), telaPrincipal(nome_usuario)]
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
        messagebox.showwarning("CAMPOS VAZIOS", "Atenção! Todos os campos devem ser preenchidos")
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
    --> Exibe a tela de confirmação com os dados preenchidos
    """
    janela_confirmacao = customtkinter.CTk()

    # Pegando a altura e largura da tela
    alturaTela = janela_confirmacao.winfo_screenheight()
    larguraTela = janela_confirmacao.winfo_screenwidth()
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    janela_confirmacao.iconbitmap("./assets/fiap-ico.ico")
    janela_confirmacao.title("CONFIRMAÇÃO DE DADOS")
    janela_confirmacao.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
    janela_confirmacao.minsize(655, 400)
    janela_confirmacao.maxsize(655, 400)

    canvas_confirmacao = Canvas(janela_confirmacao, width=655, height=400, bd=-1000)
    canvas_confirmacao.pack(fill="both", expand=True)

    imagemFundoConfirmacao = PhotoImage(file="assets/fundoLogin.png")
    canvas_confirmacao.create_image(0, 0, image=imagemFundoConfirmacao, anchor="nw")

    canvas_confirmacao.create_text(276, 115, text="Confirmação de", fill="white", font=("Arial", 22, "bold"))
    canvas_confirmacao.create_text(438, 115, text="Dados", fill="white", font=("Arial", 22, "bold"))
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
                                                               telaPrincipal(nome_usuario)])
    canvas_confirmacao.create_window(404, 300, window=botao_confirmar)

    # Printando no Terminal
    print(f"Nome: {nome_usuario}")
    print(f"Login: {login_usuario}")
    print(f"Senha: {senha_usuario}")
    print(f"Senha CMD: {senha_cmd_usuario}")

    janela_confirmacao.mainloop()


def mostrar_senha_usuario():
    """
    --> Função para mostrar e esconder a senha do monitor
    """
    # Carregando imagens (e ao mesmo tempo redimensionando)
    imagem_olho = ImageTk.PhotoImage(Image.open("./assets/olho.png").resize((20, 20)))
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open("./assets/olhoFechado.png").resize((20, 20)))
    if entrada_senha.cget('show') == '*':
        entrada_senha.configure(show='')  # Mostra a senha
        botao_mostrar_senha_usuario.configure(image=imagem_olho)  # Altera o ícone para uma imagem de um olho aberto
    else:
        entrada_senha.configure(show='*')  # Oculta a senha
        botao_mostrar_senha_usuario.configure(
            image=imagem_olho_fechado)  # Altera o ícone para uma imagem de um olho fechado


def mostrar_senha_cmd():
    """
    --> Mesma lógica da função mostrar_senha_usuario(), porém para mostrar e esconder a senha do campo do CMD
    """
    # Carregando imagens
    imagem_olho = ImageTk.PhotoImage(Image.open("./assets/olho.png").resize((20, 20)))
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open("./assets/olhoFechado.png").resize((20, 20)))
    if entrada_senha_cmd.cget('show') == '*':
        entrada_senha_cmd.configure(show='')  # Mostra a senha
        botao_mostrar_senha_cmd.configure(image=imagem_olho)  # Altera o ícone para uma imagem de um olho aberto
    else:
        entrada_senha_cmd.configure(show='*')  # Oculta a senha
        botao_mostrar_senha_cmd.configure(
            image=imagem_olho_fechado)  # Altera o ícone para uma imagem de um olho fechado


def tela_login():
    """
    --> Função para criar e exibir a tela de login.
    Chamada tanto no início quanto ao voltar da tela de confirmação.
    """
    global janela_login, entrada_nome, entrada_login, entrada_senha, entrada_senha_cmd, botao_mostrar_senha_usuario, botao_mostrar_senha_cmd  # Variáveis globais para acessar em outros momentos

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

    # Canvas2 para posicionar os elementos
    canvas2 = Canvas(janela_login, width=655, height=400, bd=-1000)
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
    entrada_nome = customtkinter.CTkEntry(janela_login, placeholder_text="Insira seu nome...", width=300,
                                          fg_color="transparent")
    canvas2.create_window(325, 103, window=entrada_nome)

    # Login do Monitor
    canvas2.create_text(293, 137, text="Login de Usuário (Runas)", fill="white", font=("Arial", 14, "bold"))
    entrada_login = customtkinter.CTkEntry(janela_login, placeholder_text="Insira o seu usuário...", width=300,
                                           fg_color="transparent")
    canvas2.create_window(325, 170, window=entrada_login)

    # Senha do Monitor
    canvas2.create_text(296, 207, text="Senha do Monitor (Runas)", fill="white", font=("Arial", 14, "bold"))
    entrada_senha = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha...", show="*", width=300,
                                           fg_color="transparent", height=35)
    canvas2.create_window(325, 240, window=entrada_senha)

    # Botão Mostrar/Ocultar Senha com Ícone
    botao_mostrar_senha_usuario = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0,
                                                          command=mostrar_senha_usuario, text="", hover_color=cor_input,
                                                          fg_color=cor_input)
    canvas2.create_window(455, 240, window=botao_mostrar_senha_usuario)  # Posição ao lado do campo de senha

    # Senha para o CMD
    canvas2.create_text(265, 278, text="Senha para o CMD:", fill="white", font=("Arial", 14, "bold"))
    entrada_senha_cmd = customtkinter.CTkEntry(janela_login, placeholder_text="Insira sua senha para o CMD...",
                                               show="*", width=300, fg_color="transparent", height=35)
    canvas2.create_window(325, 310, window=entrada_senha_cmd)

    botao_mostrar_senha_cmd = customtkinter.CTkButton(janela_login, image=imagem_olho_fechado, width=0, height=0,
                                                      command=mostrar_senha_cmd, text="", hover_color=cor_input,
                                                      fg_color=cor_input)
    canvas2.create_window(455, 310, window=botao_mostrar_senha_cmd)  # Posição ao lado do campo de senha

    # Botão Entrar
    botao_entrar = customtkinter.CTkButton(janela_login, text="Entrar", width=300, height=34, command=verificar_login,
                                           fg_color=cor_fundo, font=fonteBotao, hover_color=cor_fundo_escuro)
    canvas2.create_window(325, 355, window=botao_entrar)

    # Iniciar o loop da tela de login
    janela_login.mainloop()


tela_login()
