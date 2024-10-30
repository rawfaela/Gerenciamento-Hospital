import mysql.connector
import tkinter as tk
from tkinter import font

# Conexão com o banco de dados
conexao_banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hospital"
)

cursor = conexao_banco.cursor()

# Função para verificar se o exame já existe e cadastrar se não existir
def verificar_exame(codigo, descricao, tipo, preparo, pos_exame):
    comando_sql = f'SELECT * FROM exames WHERE codigo = "{codigo}"'
    cursor.execute(comando_sql)
    exames = cursor.fetchall()  # Obtém todos os resultados

    if exames:  # Se já existir, retorna False
        return False
    else:  # Se não existir, realiza a inserção
        cadastrar_exame(codigo, descricao, tipo, preparo, pos_exame)
        return True

# Função para cadastrar exame
def cadastrar_exame(codigo, descricao, tipo, preparo, pos_exame):
    comando_sql = f"INSERT INTO exames (codigo, descricao, tipo, preparo, pos_exame) VALUES ('{codigo}', '{descricao}', '{tipo}', '{preparo}', '{pos_exame}')"
    cursor.execute(comando_sql)
    conexao_banco.commit()

# Janela principal
janela = tk.Tk()
janela.title("Hospital Ghellere Da Silva Machado")
janela.geometry("600x400")

# Fonte
nova_fonte = font.Font(family="Arial", size=20)

# Inicializa label_resposta como None
label_resposta = None  

# Mostra a tela de cadastro
def mostrar_cadastro():
    global label_resposta  

    for widget in janela.winfo_children():
        widget.destroy()

    label_titulo = tk.Label(janela, text="Cadastro de Exame", font=nova_fonte, fg="blue")
    label_titulo.pack(pady=20)

    # Entradas para os campos necessários
    label_codigo = tk.Label(janela, text="Código:", font=nova_fonte)
    label_codigo.pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=nova_fonte)
    entrada_codigo.pack(pady=5)

    label_descricao = tk.Label(janela, text="Descrição:", font=nova_fonte)
    label_descricao.pack(pady=5)
    entrada_descricao = tk.Entry(janela, font=nova_fonte)
    entrada_descricao.pack(pady=5)

    label_tipo = tk.Label(janela, text="Tipo:", font=nova_fonte)
    label_tipo.pack(pady=5)
    entrada_tipo = tk.Entry(janela, font=nova_fonte)
    entrada_tipo.pack(pady=5)

    label_preparo = tk.Label(janela, text="Preparo:", font=nova_fonte)
    label_preparo.pack(pady=5)
    entrada_preparo = tk.Entry(janela, font=nova_fonte)
    entrada_preparo.pack(pady=5)

    label_pos_exame = tk.Label(janela, text="Pós Exame:", font=nova_fonte)
    label_pos_exame.pack(pady=5)
    entrada_pos_exame = tk.Entry(janela, font=nova_fonte)
    entrada_pos_exame.pack(pady=5)

    botao_enviar = tk.Button(janela, text="Enviar", font=nova_fonte, 
                             command=lambda: enviar_dados(
                                 entrada_codigo.get(),
                                 entrada_descricao.get(),
                                 entrada_tipo.get(),
                                 entrada_preparo.get(),
                                 entrada_pos_exame.get()
                             ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=nova_fonte, command=mostrar_menu)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def enviar_dados(codigo, descricao, tipo, preparo, pos_exame):
    global label_resposta  
    if label_resposta is not None:
        label_resposta.destroy()  
    
    if codigo.strip() and descricao.strip() and tipo.strip() and preparo.strip() and pos_exame.strip():
        if verificar_exame(codigo, descricao, tipo, preparo, pos_exame):  # Verifica e cadastra se não existir
            label_resposta = tk.Label(janela, text=f"Exame {descricao} cadastrado!", font=nova_fonte, fg="green")
        else:  # Se já existir
            label_resposta = tk.Label(janela, text="Código já cadastrado!", font=nova_fonte, fg="red")
    else:
        label_resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=nova_fonte, fg="red")
    
    label_resposta.pack(pady=20)

# Mostra o menu inicial
def mostrar_menu():
    for widget in janela.winfo_children():
        widget.destroy()
    
    label = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=nova_fonte, fg="blue", bg="lightgrey")
    label.pack(pady=20)

    botao_cadastrar = tk.Button(janela, text="CADASTRAR EXAME", font=nova_fonte, bg="green", fg="white", command=mostrar_cadastro)
    botao_cadastrar.pack(pady=10)

mostrar_menu()

janela.mainloop()

cursor.close()
conexao_banco.close()
