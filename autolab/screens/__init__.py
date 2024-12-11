import os
from tkinter import PhotoImage
from customtkinter import CTk, CTkCanvas, CTkButton

# Caminho do projeto
path = __file__.split("\\")
main = path[0] + f"\\{path[1]}\\"

def centralizar(janela, altura=400, largura=655):
    """
    --> Funcao para centralizar qualquer janela, baseado na altura e na largura da tela.
    :param: Janela que você deseja centralizar
    """

    # Centralizar janela
    alturaTela = janela.winfo_screenheight()
    larguraTela = janela.winfo_screenwidth()

    # Calculando o eixo X e Y para centralizar a janela
    eixoX = (larguraTela / 2) - (largura / 2)
    eixoY = (alturaTela / 2) - (altura / 2)

    # Definindo o tamanho e a posição da janela
    janela.geometry(f"{largura}x{altura}+{int(eixoX)}+{int(eixoY)}")
    janela.minsize(largura, altura)
    janela.maxsize(largura, altura)


# def background(canvas, caminhoImagem=os.getcwd()[0:2] + "\\bats-fiap-main\\project\\assets\\fundoFiap.png", ancoragem="nw"):
# def background(canvas, caminhoImagem=os.getcwd()[0:2] + "\\bats-fiap\\project\\assets\\fundoFiap.png", ancoragem="nw"):
def background(canvas, caminhoImagem= main + "project\\assets\\fundoFiap.png", ancoragem="nw"):
    """
    --> Funcao para definir o plano de fundo da janela atual.
    :param canvas: Canvas para disposicao da imagem de fundo
    :param caminhoImagem: Caminho para imagem que voce deseja (caso nao seja preenchido, ele utiliza a imagem de fundo padrao)
    :param ancoragem: Ancoragem da imagem no Canvas (caso nao seja preenchido, preenche o parametro com "nw")
    """
    img = PhotoImage(file=caminhoImagem)
    canvas.create_image(0, 0, image=img, anchor=ancoragem)
    canvas.img = img


def mostrar_comando_executado(janela_anterior, tela_destino, cor_botao="#ed145b", cor_hover_botao="#d01150"):
    """
    --> Funcao que exibe a mensagem de "Comando executado com sucesso!" com um botao de "Continuar"
    :param janela_anterior: Janela anterior que voce deseja fechar
    :param tela_destino: Funcao que abre a proxima tela (por exemplo, telaPrincipal, telaReiniciar, etc.)
    :param cor_botao: Cor do botao principal (padrao #ed145b)
    :param cor_hover_botao: Cor para o hover do botao principal (padrao #d01150)
    """
    # Fechando a janela anterior
    janela_anterior.destroy()

    # Criando a nova janela de sucesso
    janela_sucesso = CTk()

    janela_sucesso.iconbitmap(os.getcwd()[0:2] + "\\bats-fiap-main\\project\\assets\\fiap-ico.ico")
    # janela_sucesso.iconbitmap(os.getcwd()[0:2] + "\\bats-fiap\\project\\assets\\fiap-ico.ico")

    centralizar(janela_sucesso)

    # Canvas1 para disposicao dos elementos
    canvas1 = CTkCanvas(janela_sucesso, width=655, height=400, bd=-100000)
    canvas1.pack(fill="both", expand=True)

    # Imagem de Fundo
    background(canvas1, os.getcwd()[0:2] + "\\bats-fiap-main\\project\\assets\\fundoFiap.png")
    # background(canvas1, os.getcwd()[0:2] + "\\bats-fiap\\project\\assets\\fundoFiap.png")

    # Título da janela
    janela_sucesso.title("SUCESSO")

    # Mensagem
    canvas1.create_text(325, 125, text="Comando Executado", fill="white", font=("Arial", 30, "bold"))
    canvas1.create_text(325, 167, text="com Sucesso!", fill=cor_botao, font=("Arial", 30, "bold"))

    # Botao "Continuar"
    botao_continuar = CTkButton(
        janela_sucesso,
        text="Continuar",
        width=275,
        height=80,
        fg_color=cor_botao,
        hover_color=cor_hover_botao,
        font=("Arial", 26, "bold"),
        command=lambda: [janela_sucesso.destroy(), tela_destino()]  # Chama a tela de destino passada como argumento
    )
    canvas1.create_window(325, 260, window=botao_continuar)

    # Exibindo a janela de sucesso
    janela_sucesso.mainloop()
