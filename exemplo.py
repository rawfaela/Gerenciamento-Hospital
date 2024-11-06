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

verdinho = '#B8DAC2'
cinza = '#7D7E80'
bege = '#DDCCBB'
azulclaro = '#0087A0'
azulescuro = '#336182'

def verificar_consultas(codigo, data, hora, tipo, codpaciente, codmedico, codexame):
    comando_sql = f'SELECT * FROM consultas WHERE codigo = "{codigo}"'
    cursor.execute(comando_sql)
    consulta = cursor.fetchall()

    if consulta: 
        return False
    else: 
        cadastrar_consultas(codigo, data, hora, tipo, codpaciente, codmedico, codexame)
        return True
    
def cadastrar_consultas(codigo, data, hora, tipo, codpaciente, codmedico, codexame):
    comando_sql = f'INSERT INTO consultas (codigo, data, hora, tipo, codpaciente, codmedico, codexame) VALUES ({codigo},"{data}","{hora}","{tipo}",{codpaciente},{codmedico},{codexame})'
    cursor.execute(comando_sql)
    conexao_banco.commit()
 
janela = tk.Tk()
janela.title("Hospital Ghellere Da Silva Machado") 
janela.state("zoomed") #tela cheia
janela.configure(background=bege)

# Fonte
fonte = font.Font(family="Arial", size=20)
ftitulo = font.Font(family="Arial", size=25, weight="bold")

resposta = None 
def cadastro_consultas():
    global resposta  

    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de Consultas", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    def next_entry(event, next_widget):
        next_widget.focus()

    codigo = tk.Label(janela, text="Código:", font=fonte)
    codigo.pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=fonte)
    entrada_codigo.pack(pady=5)

    data = tk.Label(janela, text="Data:", font=fonte)
    data.pack(pady=5)
    entrada_data = tk.Entry(janela, font=fonte)
    entrada_data.pack(pady=5)

    hora = tk.Label(janela, text="Hora:", font=fonte)
    hora.pack(pady=5)
    entrada_hora = tk.Entry(janela, font=fonte)
    entrada_hora.pack(pady=5)

    tipo = tk.Label(janela, text="Tipo:", font=fonte)
    tipo.pack(pady=5)
    entrada_tipo = tk.Entry(janela, font=fonte)
    entrada_tipo.pack(pady=5)

    codpaciente = tk.Label(janela, text="Código Paciente:", font=fonte)
    codpaciente.pack(pady=5)
    entrada_codpaciente = tk.Entry(janela, font=fonte)
    entrada_codpaciente.pack(pady=5)

    codmedico = tk.Label(janela, text="Código Médico:", font=fonte)
    codmedico.pack(pady=5)
    entrada_codmedico = tk.Entry(janela, font=fonte)
    entrada_codmedico.pack(pady=5)

    codexame = tk.Label(janela, text="Código Exame:", font=fonte)
    codexame.pack(pady=5)
    entrada_codexame = tk.Entry(janela, font=fonte)
    entrada_codexame.pack(pady=5)

    entrada_codigo.bind("<Return>", lambda event: next_entry(event, entrada_data))
    entrada_data.bind("<Return>", lambda event: next_entry(event, entrada_hora))
    entrada_hora.bind("<Return>", lambda event: next_entry(event, entrada_tipo))
    entrada_tipo.bind("<Return>", lambda event: next_entry(event, entrada_codpaciente))
    entrada_codpaciente.bind("<Return>", lambda event: next_entry(event, entrada_codmedico))
    entrada_codmedico.bind("<Return>", lambda event: next_entry(event, entrada_codexame))
    entrada_codexame.bind("<Return>", lambda event: enviar_dados_consultas(     
     entrada_codigo.get(),
     entrada_data.get(),
     entrada_hora.get(),
     entrada_tipo.get(),
     entrada_codpaciente.get(),
     entrada_codmedico.get(),
     entrada_codexame.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: enviar_dados_consultas(
        entrada_codigo.get(),
        entrada_data.get(),
        entrada_hora.get(),
        entrada_tipo.get(),
        entrada_codpaciente.get(),
        entrada_codmedico.get(),
        entrada_codexame.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def enviar_dados_consultas(codigo, data, hora, tipo, codpaciente, codmedico, codexame):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if codigo.strip() and data.strip() and hora.strip() and tipo.strip() and codpaciente.strip() and codmedico.strip() and codexame.strip():
        if verificar_consultas(codigo, data, hora, tipo, codpaciente, codmedico, codexame):  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text=f"consulta do código: {codigo} cadastrado!", font=fonte, fg="pink")
        else: 
            resposta = tk.Label(janela, text="código já cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

def menu():
    for widget in janela.winfo_children():
        widget.destroy()
    
    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_cadastro_c= tk.Button(janela, text="CADASTRAR CONSULTAS", font=fonte, bg=azulclaro, fg="black", command=cadastro_consultas)
    botao_cadastro_c.pack(pady=10)

menu()
janela.mainloop()

cursor.close()
conexao_banco.close()