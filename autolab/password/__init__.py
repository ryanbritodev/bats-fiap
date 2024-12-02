import os
from PIL import ImageTk, Image
from tkinter import messagebox


def mostrarSenha(entradaSenha, botaoMostrarSenha):
    """
    --> Funcao para mostrar e esconder a senha do monitor
    !!! USAR LAMBDA !!!
    :param entradaSenha: Campo de entrada de senha
    :param botaoMostrarSenha: Botao para esconder e mostar a senha
    """
    # Variaveis globais para imagens de olho aberto e fechado
    imagem_olho = ImageTk.PhotoImage(Image.open(os.getcwd()[0:2] + "\\bats-fiap-main\\project\\assets\\olho.png").resize((20, 20)))
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open(os.getcwd()[0:2] + "\\bats-fiap-main\\project\\assets\\olhoFechado.png").resize((20, 20)))
    if entradaSenha.cget('show') == '*':
        entradaSenha.configure(show='')  # Mostra a senha
        botaoMostrarSenha.configure(image=imagem_olho)  # Altera o icone para uma imagem de um olho aberto
    else:
        entradaSenha.configure(show='*')  # Oculta a senha
        botaoMostrarSenha.configure(image=imagem_olho_fechado)  # Altera o icone para uma imagem de um olho fechado


def verificar_campos_vazios(login, senha):
    """
    --> Funcao que verifica se os campos de login e senha estao preenchidos.
    :param login: Login personalizado do usuario
    :param senha: Senha personalizada do usuario
    """
    if not login.strip() or not senha.strip():  # Verifica se os campos estão vazios ou com espaços em branco
        messagebox.showwarning("CAMPOS VAZIOS", "Atenção! Todos os campos devem ser preenchidos.")
        return False
    return True
