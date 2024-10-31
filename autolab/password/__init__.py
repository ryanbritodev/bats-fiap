from PIL import ImageTk, Image


def mostrarSenha(entradaSenha, botaoMostrarSenha):
    """
    --> Funcao para mostrar e esconder a senha do monitor
    !!! USAR LAMBDA !!!
    :param entradaSenha: Campo de entrada de senha
    :param botaoMostrarSenha: Botao para esconder e mostar a senha
    """
    # Variaveis globais para imagens de olho aberto e fechado
    imagem_olho = ImageTk.PhotoImage(Image.open("./assets/olho.png").resize((20, 20)))
    imagem_olho_fechado = ImageTk.PhotoImage(Image.open("./assets/olhoFechado.png").resize((20, 20)))
    if entradaSenha.cget('show') == '*':
        entradaSenha.configure(show='')  # Mostra a senha
        botaoMostrarSenha.configure(image=imagem_olho)  # Altera o icone para uma imagem de um olho aberto
    else:
        entradaSenha.configure(show='*')  # Oculta a senha
        botaoMostrarSenha.configure(image=imagem_olho_fechado)  # Altera o icone para uma imagem de um olho fechado
