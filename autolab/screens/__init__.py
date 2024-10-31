from tkinter import PhotoImage


def centralizar(janela):
    """
    --> Funcao para centralizar qualquer janela, baseado na altura e na largura da tela.
    :param: Janela que você deseja centralizar
    """
    # Altura e Largura da Janela
    altura = 400
    largura = 655

    # Centralizar janela
    alturaTela = janela.winfo_screenheight()
    larguraTela = janela.winfo_screenwidth()

    # Calculando o eixo X e Y para centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janela.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
    janela.minsize(655, 400)
    janela.maxsize(655, 400)


def background(canvas, caminhoImagem="assets/fundoFiap.png", ancoragem="nw"):
    """
    --> Funcao para definir o plano de fundo da janela atual.
    :param canvas: Canvas para disposicao da imagem de fundo
    :param caminhoImagem: Caminho para imagem que voce deseja (caso nao seja preenchido, ele utiliza a imagem de fundo padrao)
    :param ancoragem: Ancoragem da imagem no Canvas (caso nao seja preenchido, preenche o parametro com "nw")
    """
    img = PhotoImage(file=caminhoImagem)
    canvas.create_image(0, 0, image=img, anchor=ancoragem)
    canvas.img = img
