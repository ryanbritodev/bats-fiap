# FIAP AUTOLAB
# IMPORTANTE: se você achou este pen drive, NÃO EXECUTE OS COMANDOS, eles servem
# única e exclusivamente para auxílio de monitores, utilizá-los indevidamente pode acarretar
# em problemas sérios.
# Créditos:
# Victor Flávio Demarchi Viana
# Ryan Brito Pereira Ramos

import os
from tkinter import Canvas, PhotoImage, messagebox
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")

altura = 400
largura = 655

# Fonte e Cores
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
        entry.delete(0, customtkinter.END)
        entry.insert(0, str(current_value + 1))
        janela.after(100, increment)


# Função para diminuir o valor
def decrement():
    if decrementing:
        current_value = int(entry.get())
        if current_value > 1:
            entry.delete(0, customtkinter.END)
            entry.insert(0, str(current_value - 1))
        else:
            messagebox.showerror("Erro", "O valor deve ser maior que 0.")
            entry.delete(0, customtkinter.END)
            entry.insert(0, "1")
        janela.after(100, decrement)


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

    # Canvas1
    canvas1 = Canvas(janela, width=655, height=400, bd=-100)
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

    # Ideias de Botões (sem o parâmetro "command" pra executar os bats, por enquanto)
    botao_desligar = customtkinter.CTkButton(janela, text="Desligar", width=130, height=40, font=fonteBotaoP,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro,
                                             command=lambda: [janela.destroy(), telaDesligar()])
    botao_reiniciar = customtkinter.CTkButton(janela, text="Reiniciar", width=130, height=40, font=fonteBotaoP,
                                              fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_limpar = customtkinter.CTkButton(janela, text="Limpar o (D:)", width=130, height=40, font=fonteBotaoP,
                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_copiar = customtkinter.CTkButton(janela, text="Copiar Arquivo", width=130, height=40, font=fonteBotaoP,
                                           fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_pon = customtkinter.CTkButton(janela, text="Logar PON", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_pn = customtkinter.CTkButton(janela, text="Logar PN", width=130, height=40, font=fonteBotaoP,
                                       fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_nac = customtkinter.CTkButton(janela, text="Abrir NAC", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_mensagem = customtkinter.CTkButton(janela, text="Mensagem", width=130, height=40, font=fonteBotaoP,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_logar = customtkinter.CTkButton(janela, text="Logar Usuário", width=130, height=40, font=fonteBotaoP,
                                          fg_color=cor_fundo, hover_color=cor_fundo_escuro)
    botao_url = customtkinter.CTkButton(janela, text="Abrir URL", width=130, height=40, font=fonteBotaoP,
                                        fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(118, 250, window=botao_desligar)
    canvas1.create_window(118, 300, window=botao_reiniciar)
    canvas1.create_window(118, 350, window=botao_logar)
    canvas1.create_window(258, 250, window=botao_limpar)
    canvas1.create_window(258, 300, window=botao_copiar)
    canvas1.create_window(258, 350, window=botao_url)
    canvas1.create_window(398, 250, window=botao_pon)
    canvas1.create_window(398, 300, window=botao_pn)
    canvas1.create_window(398, 350, window=botao_nac)
    canvas1.create_window(538, 250, window=botao_mensagem)

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

    # Canvas1
    canvas1 = Canvas(janelaDesligar, width=655, height=400, bd=-100)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    fundo = PhotoImage(file="./assets/fundoFiap.png")
    canvas1.create_image(0, 0, image=fundo, anchor="nw")

    # Imagem Shutdown
    shutdown = PhotoImage(file="assets/autoSHUTDOWN.png")
    canvas1.create_image(328, 70, image=shutdown)

    # Desligar Lab Inteiro
    canvas1.create_text(120, 185, text="Desligar Lab", fill="white", font=("Arial", 21, "bold"))
    botao_desligar_lab_inteiro = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50, font=fonte,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro, command=enviar)

    # Campo de entrada numérica
    global entry
    entry = customtkinter.CTkEntry(janelaDesligar, width=100, justify="center", fg_color=cor_fundo, font=fonte)
    entry.insert(0, "1")  # Valor inicial
    canvas1.create_window(328, 200, window=entry)

    # Botões de aumentar e diminuir o valor
    increase_button = customtkinter.CTkButton(janelaDesligar, text="▲", width=30)
    canvas1.create_window(380, 200, window=increase_button)
    increase_button.bind("<ButtonPress-1>", start_increment)
    increase_button.bind("<ButtonRelease-1>", stop_increment)

    decrease_button = customtkinter.CTkButton(janelaDesligar, text="▼", width=30)
    canvas1.create_window(276, 200, window=decrease_button)
    decrease_button.bind("<ButtonPress-1>", start_decrement)
    decrease_button.bind("<ButtonRelease-1>", stop_decrement)

    # Desligar Máquina
    canvas1.create_text(328, 140, text="Desligar Máquina", fill="white", font=("Arial", 16, "bold"))
    botao_desligar_maquina = customtkinter.CTkButton(janelaDesligar, text="Desligar", width=170, height=50, font=fonte,
                                             fg_color=cor_fundo, hover_color=cor_fundo_escuro)

    # Posicionando os botões sobre o Canvas
    canvas1.create_window(120, 235, window=botao_desligar_lab_inteiro)
    canvas1.create_window(328, 295, window=botao_desligar_maquina)

    # Loop da Janela principal
    janelaDesligar.mainloop()


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

    canvas_confirmacao = Canvas(janela_confirmacao, width=655, height=400, bd=-100)
    canvas_confirmacao.pack(fill="both", expand=True)

    imagemFundoConfirmacao = PhotoImage(file="assets/fundoLogin.png")
    canvas_confirmacao.create_image(0, 0, image=imagemFundoConfirmacao, anchor="nw")

    canvas_confirmacao.create_text(276, 115, text="Confirmação de", fill="white", font=("Arial", 22, "bold"))
    canvas_confirmacao.create_text(438, 115, text="Dados", fill=cor_fundo, font=("Arial", 22, "bold"))
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
    # Carregando imagens
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

    # Canvas
    canvas2 = Canvas(janela_login, width=655, height=400, bd=-100)
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
