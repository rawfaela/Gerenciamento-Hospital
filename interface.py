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

# Função para verificar se o exame já existe e cadastrar se não existir
def verificar_exame(codigo, descricao, tipo, preparo, pos_exame):
    comando_sql = f'SELECT * FROM exames WHERE codigo = {codigo}'
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

def verificar_paciente(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil):
    comando_sql = f'SELECT * FROM pacientes WHERE cpf = "{cpf}"'
    cursor.execute(comando_sql)
    pacientes = cursor.fetchall()  # Obtém todos os resultados

    if pacientes:  # Se já existir, retorna False
        return False
    else:  # Se não existir, realiza a inserção
        cadastrar_paciente(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil)
        return True

# Função para cadastrar paciente
def cadastrar_paciente(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil):
    comando_sql = f"INSERT INTO pacientes (cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil) VALUES ('{cpf}', '{nome}', '{telefone}', '{endereco}', '{cidade}', '{estado}', '{sexo}', '{datanasc}', '{estadocivil}')"
    cursor.execute(comando_sql)
    conexao_banco.commit()

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
    comando_sql = f'INSERT INTO consultas (codigo, data, hora, tipo, codpaciente, codmedico, codexame) VALUES ({codigo},"{data}","{hora}00","{tipo}",{codpaciente},{codmedico},{codexame})'
    cursor.execute(comando_sql)
    conexao_banco.commit()

def verificar_medicos(crm, nome, telefone, endereco, cidade, estado, especialidade):
    comando_sql = f'SELECT * FROM medicos WHERE crm = "{crm}"'
    cursor.execute(comando_sql)
    medicos = cursor.fetchall()  # Obtém todos os resultados

    if medicos:  # Se já existir, retorna False
        return False
    else:  # Se não existir, realiza a inserção
        cadastrar_medicos(crm, nome, telefone, endereco, cidade, estado, especialidade)
        return True

# Função para cadastrar médico
def cadastrar_medicos(crm, nome, telefone, endereco, cidade, estado, especialidade):
    comando_sql = f"INSERT INTO medicos (crm, nome, telefone, endereco, cidade, estado, especialidade) VALUES ('{crm}', '{nome}', '{telefone}', '{endereco}', '{cidade}', '{estado}', '{especialidade}')"
    cursor.execute(comando_sql)
    conexao_banco.commit()

# Janela principal
janela = tk.Tk()
janela.title("Hospital Ghellere Da Silva Machado")  #titulo da janela
janela.state("zoomed") #tela cheia
janela.configure(background=bege)

# Fonte
fonte = font.Font(family="Arial", size=20)
ftitulo = font.Font(family="Arial", size=25, weight="bold")

# Inicializa resposta como None
resposta = None  

# Mostra a tela de cadastro
def cadastro_exame():
    global resposta  

    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de Exame", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    def next_entry(event, next_widget):
        next_widget.focus()

    # Entradas para os campos necessários
    codigo = tk.Label(janela, text="Código:", font=fonte)
    codigo.pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=fonte)
    entrada_codigo.pack(pady=5)

    descricao = tk.Label(janela, text="Descrição:", font=fonte)
    descricao.pack(pady=5)
    entrada_descricao = tk.Entry(janela, font=fonte)
    entrada_descricao.pack(pady=5)

    tipo = tk.Label(janela, text="Tipo:", font=fonte)
    tipo.pack(pady=5)
    entrada_tipo = tk.Entry(janela, font=fonte)
    entrada_tipo.pack(pady=5)

    preparo = tk.Label(janela, text="Preparo:", font=fonte)
    preparo.pack(pady=5)
    entrada_preparo = tk.Entry(janela, font=fonte)
    entrada_preparo.pack(pady=5)

    pos_exame = tk.Label(janela, text="Pós Exame:", font=fonte)
    pos_exame.pack(pady=5)
    entrada_pos_exame = tk.Entry(janela, font=fonte)
    entrada_pos_exame.pack(pady=5)

    entrada_codigo.bind("<Return>", lambda event: next_entry(event, entrada_descricao))
    entrada_descricao.bind("<Return>", lambda event: next_entry(event, entrada_tipo))
    entrada_tipo.bind("<Return>", lambda event: next_entry(event, entrada_preparo))
    entrada_preparo.bind("<Return>", lambda event: next_entry(event, entrada_pos_exame))
    entrada_pos_exame.bind("<Return>", lambda _: enviar_dados(
        entrada_codigo.get(),
        entrada_descricao.get(),
        entrada_tipo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: enviar_dados(
        entrada_codigo.get(),
        entrada_descricao.get(),
        entrada_tipo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def enviar_dados(codigo, descricao, tipo, preparo, pos_exame):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if codigo.strip() and descricao and tipo and preparo and pos_exame:
        if verificar_exame(codigo, descricao, tipo, preparo, pos_exame):  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text=f"Exame {descricao} cadastrado!", font=fonte, fg="pink")
        else:  # Se já existir
            resposta = tk.Label(janela, text="Código já cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

def cadastro_paciente():
    global resposta  

    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de paciente", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    def next_entry(event, next_widget):
        next_widget.focus()

    # Entradas para os campos necessários
    cpf = tk.Label(janela, text="CPF:", font=fonte)
    cpf.pack(pady=5)
    entrada_cpf = tk.Entry(janela, font=fonte)
    entrada_cpf.pack(pady=5)

    nome = tk.Label(janela, text="Nome:", font=fonte)
    nome.pack(pady=5)
    entrada_nome = tk.Entry(janela, font=fonte)
    entrada_nome.pack(pady=5)

    telefone = tk.Label(janela, text="Telefone:", font=fonte)
    telefone.pack(pady=5)
    entrada_telefone = tk.Entry(janela, font=fonte)
    entrada_telefone.pack(pady=5)

    endereco = tk.Label(janela, text="Endereço:", font=fonte)
    endereco.pack(pady=5)
    entrada_endereco = tk.Entry(janela, font=fonte)
    entrada_endereco.pack(pady=5)

    cidade = tk.Label(janela, text="Cidade:", font=fonte)
    cidade.pack(pady=5)
    entrada_cidade = tk.Entry(janela, font=fonte)
    entrada_cidade.pack(pady=5)

    estado = tk.Label(janela, text="Estado:", font=fonte)
    estado.pack(pady=5)
    entrada_estado = tk.Entry(janela, font=fonte)
    entrada_estado.pack(pady=5)

    sexo = tk.Label(janela, text="Sexo:", font=fonte)
    sexo.pack(pady=5)
    entrada_sexo = tk.Entry(janela, font=fonte)
    entrada_sexo.pack(pady=5)

    datanasc = tk.Label(janela, text="Data de nascimento:", font=fonte)
    datanasc.pack(pady=5)
    entrada_datanasc = tk.Entry(janela, font=fonte)
    entrada_datanasc.pack(pady=5)

    estadocivil = tk.Label(janela, text="Estado civil:", font=fonte)
    estadocivil.pack(pady=5)
    entrada_estadocivil = tk.Entry(janela, font=fonte)
    entrada_estadocivil.pack(pady=5)

    entrada_cpf.bind("<Return>", lambda event: next_entry(event, entrada_nome))
    entrada_nome.bind("<Return>", lambda event: next_entry(event, entrada_telefone))
    entrada_telefone.bind("<Return>", lambda event: next_entry(event, entrada_endereco))
    entrada_endereco.bind("<Return>", lambda event: next_entry(event, entrada_cidade))
    entrada_cidade.bind("<Return>", lambda event: next_entry(event, entrada_estado))
    entrada_estado.bind("<Return>", lambda event: next_entry(event, entrada_sexo))
    entrada_sexo.bind("<Return>", lambda event: next_entry(event, entrada_datanasc))
    entrada_datanasc.bind("<Return>", lambda event: next_entry(event, entrada_estadocivil))
    entrada_estadocivil.bind("<Return>", lambda _: enviar_dados_paciente(
        entrada_cpf.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_sexo.get(),
        entrada_datanasc.get(),
        entrada_estadocivil.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: enviar_dados_paciente(
        entrada_cpf.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_sexo.get(),
        entrada_datanasc.get(),
        entrada_estadocivil.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def enviar_dados_paciente(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if cpf.strip() and nome and telefone.strip() and endereco and cidade.strip() and estado.strip() and sexo.strip() and datanasc.strip() and estadocivil.strip():
        if verificar_paciente(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil):  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text=f"Paciente {nome} cadastrado!", font=fonte, fg="pink")
        else:  # Se já existir
            resposta = tk.Label(janela, text="CPF já cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

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

def cadastro_medicos():
    global resposta  

    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de médico", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    def next_entry(event, next_widget):
        next_widget.focus()

    # Entradas para os campos necessários
    crm = tk.Label(janela, text="CRM:", font=fonte)
    crm.pack(pady=5)
    entrada_crm = tk.Entry(janela, font=fonte)
    entrada_crm.pack(pady=5)

    nome = tk.Label(janela, text="Nome:", font=fonte)
    nome.pack(pady=5)
    entrada_nome = tk.Entry(janela, font=fonte)
    entrada_nome.pack(pady=5)

    telefone = tk.Label(janela, text="Telefone:", font=fonte)
    telefone.pack(pady=5)
    entrada_telefone = tk.Entry(janela, font=fonte)
    entrada_telefone.pack(pady=5)

    endereco = tk.Label(janela, text="Endereço:", font=fonte)
    endereco.pack(pady=5)
    entrada_endereco = tk.Entry(janela, font=fonte)
    entrada_endereco.pack(pady=5)

    cidade = tk.Label(janela, text="Cidade:", font=fonte)
    cidade.pack(pady=5)
    entrada_cidade = tk.Entry(janela, font=fonte)
    entrada_cidade.pack(pady=5)

    estado = tk.Label(janela, text="Estado:", font=fonte)
    estado.pack(pady=5)
    entrada_estado = tk.Entry(janela, font=fonte)
    entrada_estado.pack(pady=5)

    especialidade = tk.Label(janela, text="Especialidade:", font=fonte)
    especialidade.pack(pady=5)
    entrada_especialidade = tk.Entry(janela, font=fonte)
    entrada_especialidade.pack(pady=5)

    entrada_crm.bind("<Return>", lambda event: next_entry(event, entrada_nome))
    entrada_nome.bind("<Return>", lambda event: next_entry(event, entrada_telefone))
    entrada_telefone.bind("<Return>", lambda event: next_entry(event, entrada_endereco))
    entrada_endereco.bind("<Return>", lambda event: next_entry(event, entrada_cidade))
    entrada_cidade.bind("<Return>", lambda event: next_entry(event, entrada_estado))
    entrada_estado.bind("<Return>", lambda event: next_entry(event, entrada_especialidade))
    entrada_especialidade.bind("<Return>", lambda _: enviar_dados_medicos(
        entrada_crm.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_especialidade.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: enviar_dados_medicos(
        entrada_crm.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_especialidade.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def enviar_dados_medicos(crm, nome, telefone, endereco, cidade, estado, especialidade):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if crm.strip() and nome.strip() and telefone.strip() and endereco.strip() and cidade.strip() and estado.strip() and especialidade.strip():
        if verificar_medicos(crm, nome, telefone, endereco, cidade, estado, especialidade):  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text=f"Médico {nome} cadastrado!", font=fonte, fg="pink")
        else:  # Se já existir
            resposta = tk.Label(janela, text="Médico já cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

# Mostra o menu inicial
def menu():
    for widget in janela.winfo_children():
        widget.destroy()
    
    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_cadastrar_e = tk.Button(janela, text="Cadastrar Exame", font=fonte, bg=azulclaro, fg="black", command=cadastro_exame)
    botao_cadastrar_e.pack(pady=10)

    botao_cadastrar_p = tk.Button(janela, text="Cadastrar Paciente", font=fonte, bg=azulclaro, fg="black", command=cadastro_paciente)
    botao_cadastrar_p.pack(pady=10)

    botao_cadastrar_c= tk.Button(janela, text="Cadastrar Consultas", font=fonte, bg=azulclaro, fg="black", command=cadastro_consultas)
    botao_cadastrar_c.pack(pady=10)

    botao_cadastrar_m= tk.Button(janela, text="Cadastrar Médicos", font=fonte, bg=azulclaro, fg="black", command=cadastro_medicos)
    botao_cadastrar_m.pack(pady=10)

menu()

janela.mainloop()

cursor.close()
conexao_banco.close()
