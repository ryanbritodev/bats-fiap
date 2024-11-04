from tkinter import messagebox


def executar_acao(tipo_acao, categoria, tempo=5, maquina=1, inicio=1, fim=40, passo=1):
    """
    --> Funcao generica para realizar acoes dos botoes dos comandos
    :param tipo_acao: Acao que voce deseja realizar (string contendo o nome da acao)
    :param categoria: Categoria da acao que voce deseja realizar (maquina, lab ou personalizado)
    :param tempo: Tempo para realizar a acao (padrao 5 segundos)
    :param maquina: Maquina individual que voce deseja realizar a acao
    :param inicio: Inicio da acao
    :param fim: Fim da acao
    :param passo: Passo para realizar a acao
    """
    # Verifica se o tempo é válido
    if tempo is None or not tempo.isdigit() or tempo == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o tempo!")
        return

    # Verifica se o campo de máquina é válido quando necessário
    if categoria == "Maquina" and (maquina is None or not maquina.isdigit() or maquina == "0"):
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para a máquina!")
        return

    # Verifica campos de início, fim e passo para ações personalizadas
    if categoria == "Personalizado":
        if inicio is None or not inicio.isdigit() or inicio == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o início!")
            return
        if fim is None or not fim.isdigit() or fim == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o fim!")
            return
        if passo is None or not passo.isdigit() or passo == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o passo!")
            return

    # Formatação das mensagens
    if categoria == "Lab":
        print(f"Tempo para {tipo_acao} Lab: {tempo}s")
    elif categoria == "Maquina":
        print(f"Máquina: {maquina}")
        print(f"Tempo para {tipo_acao}: {tempo}s")
    elif categoria == "Personalizado":
        print(f"Início: {inicio}")
        print(f"Fim: {fim}")
        print(f"Passo: {passo}")
        print(f"Tempo para {tipo_acao}: {tempo}s")
