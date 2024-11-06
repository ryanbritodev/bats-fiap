from tkinter import messagebox


def executar_acao(tipo_acao, categoria, tempo="5", maquina="1", inicio="1", fim="40", passo="1"):
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
    # Verifica se o tempo e valido
    if tempo.strip() is None or not tempo.isdigit() or tempo.strip() == "0":
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o tempo!")
        return

    # Verifica se o campo de maquina e valido quando necessario
    if categoria.strip().title() == "Maquina" and (maquina.strip() is None or not maquina.strip().isdigit() or maquina.strip() == "0"):
        messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para a máquina!")
        return

    # Verifica campos de inicio, fim e passo para acoes personalizadas
    if categoria.strip().title() == "Personalizado":
        if inicio.strip() is None or not inicio.strip().isdigit() or inicio.strip() == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o início!")
            return
        if fim.strip() is None or not fim.strip().isdigit() or fim.strip() == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o fim!")
            return
        if passo.strip() is None or not passo.strip().isdigit() or passo.strip() == "0":
            messagebox.showerror("ERRO", "Por favor, insira um valor numérico válido para o passo!")
            return

    # Formatacao das mensagens
    if categoria.strip().title() == "Lab":
        print(f"Tempo para {tipo_acao} Lab: {tempo}s")
    elif categoria.strip().title() == "Maquina":
        print(f"Máquina: {maquina}")
        print(f"Tempo para {tipo_acao}: {tempo}s")
    elif categoria.strip().title() == "Personalizado":
        print(f"Início: {inicio}")
        print(f"Fim: {fim}")
        print(f"Passo: {passo}")
        print(f"Tempo para {tipo_acao}: {tempo}s")
