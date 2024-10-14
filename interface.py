import tkinter as tk
from tkinter import PhotoImage
from tkinter import Canvas
import os

def executar_comando_desligar():
    os.system("shutdown.bat")  # Substitua pelo caminho do seu arquivo .bat

def executar_comando_ligar():
    os.system("ligar.bat")  # Substitua pelo caminho do seu arquivo .bat

def executar_comando_logar():
    os.system("logar.bat")  # Substitua pelo caminho do seu arquivo .bat

# Criando a janela principal
janela = tk.Tk()

# Tamanho da Janela
janela.geometry("600x600")

# Título
janela.title("FIAP Autobats")

# Criando Canvas
canvas1 = Canvas(janela, width=600, height=600)
canvas1.pack(fill="both", expand=True)

# Carregar e exibir imagem de fundo
imagemFundo = PhotoImage(file="fundoFiap.png")
canvas1.create_image(0, 0, image=imagemFundo, anchor="nw")

# Carregar o logo da FIAP e posicioná-lo
logoFiap = PhotoImage(file="fiapLogo.png")
canvas1.create_image(300, 100, image=logoFiap)

# Cores dos Botões
cor_fundo = "#e4336c"  # Cor de fundo
cor_texto = "white"  # Cor do texto

# Fonte
fonte = ("", 12, "bold")

# Criando botões no Canvas
botao_desligar = tk.Button(janela, text="Desligar", command=executar_comando_desligar, width=15, bg=cor_fundo, fg=cor_texto, font=fonte)
botao_ligar = tk.Button(janela, text="Ligar", command=executar_comando_ligar, width=15,  bg=cor_fundo, fg=cor_texto, font=fonte)
botao_logar = tk.Button(janela, text="Logar", command=executar_comando_logar, width=15,  bg=cor_fundo, fg=cor_texto, font=fonte)

# Posicionando os botões sobre o Canvas
canvas1.create_window(300, 300, window=botao_desligar)  # Posição central no Canvas
canvas1.create_window(300, 350, window=botao_ligar)     # Ajuste a posição de acordo
canvas1.create_window(300, 400, window=botao_logar)

# Iniciando o loop da interface
janela.mainloop()
