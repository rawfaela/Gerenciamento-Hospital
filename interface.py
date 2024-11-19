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
#!! MUDAR ALTERAR (nao muda tudo, se entra em um if nai entra ni outro)
#!!!!! se der merda recolocar "global resposta" em cada cadastro_ no comeco
# !!!  diminuir as defds (juntar e fazer uma pra cada -- mais o)
cursor = conexao_banco.cursor()

verdinho = '#B8DAC2'
cinza = '#7D7E80'
bege = '#DDCCBB'
azulclaro = '#0087A0'
azulescuro = '#336182'

# Janela principal
janela = tk.Tk()
janela.title("Hospital Ghellere Da Silva Machado")  #titulo da janela
janela.state("zoomed") #tela cheia
janela.configure(background=bege)


fonte = font.Font(family="Arial", size=20)
ftitulo = font.Font(family="Arial", size=25, weight="bold")

resposta = None  
botao_sim = None 
infos = []

# Mostra o menu inicial
def menu():
    for widget in janela.winfo_children():
        widget.destroy()
    
    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_cadastrar = tk.Button(janela, text="Cadastrar", font=fonte, bg=azulclaro, fg="black", command=cadastrar)
    botao_cadastrar.pack(pady=10)   

    botao_alterar = tk.Button(janela, text="Alterar", font=fonte, bg=azulclaro, fg="black", command=alterar)
    botao_alterar.pack(pady=10) 

    botao_excluir = tk.Button(janela, text="Excluir", font=fonte, bg=azulclaro, fg="black", command=excluir)
    botao_excluir.pack(pady=10)  

    botao_visualizar = tk.Button(janela, text="Visualizar", font=fonte, bg=azulclaro, fg="black", command=visualizar)
    botao_visualizar.pack(pady=10) 

def cadastrar():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_cadastrar_e = tk.Button(janela, text="Cadastrar Exames", font=fonte, bg=azulclaro, fg="black", command=cadastro_exames)
    botao_cadastrar_e.pack(pady=10)

    botao_cadastrar_p = tk.Button(janela, text="Cadastrar Pacientes", font=fonte, bg=azulclaro, fg="black", command=cadastro_pacientes)
    botao_cadastrar_p.pack(pady=10)

    botao_cadastrar_c= tk.Button(janela, text="Cadastrar Consultas", font=fonte, bg=azulclaro, fg="black", command=cadastro_consultas)
    botao_cadastrar_c.pack(pady=10)

    botao_cadastrar_m= tk.Button(janela, text="Cadastrar Médicos", font=fonte, bg=azulclaro, fg="black", command=cadastro_medicos)
    botao_cadastrar_m.pack(pady=10)    

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)


def cadastro_exames():
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
    entrada_pos_exame.bind("<Return>", lambda _: enviar_dados_exames(
        entrada_codigo.get(),
        entrada_descricao.get(),
        entrada_tipo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: enviar_dados_exames(
        entrada_codigo.get(),
        entrada_descricao.get(),
        entrada_tipo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def enviar_dados_exames(codigo, descricao, tipo, preparo, pos_exame):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if codigo.strip() and descricao and tipo and preparo and pos_exame:
        comando_sql = f'SELECT * FROM exames WHERE codigo = {codigo}'
        cursor.execute(comando_sql)
        exames = cursor.fetchall() 
        if exames:  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text="Código já cadastrado!", font=fonte, fg="red")
        else:
            comando_sql = f"INSERT INTO exames (codigo, descricao, tipo, preparo, pos_exame) VALUES ('{codigo}', '{descricao}', '{tipo}', '{preparo}', '{pos_exame}')"
            cursor.execute(comando_sql)
            conexao_banco.commit() 
            resposta = tk.Label(janela, text=f"Exame {descricao} cadastrado!", font=fonte, fg="pink")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)
# Envia os dados para o banco de dados 



def cadastro_pacientes():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de Paciente", font=ftitulo, fg=azulescuro, bg=bege)
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
    entrada_estadocivil.bind("<Return>", lambda _: enviar_dados_pacientes(
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
    command=lambda: enviar_dados_pacientes(
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

def enviar_dados_pacientes(cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if cpf.strip() and nome and telefone.strip() and endereco and cidade and estado.strip() and sexo.strip() and datanasc.strip() and estadocivil.strip():
        comando_sql = f'SELECT * FROM pacientes WHERE cpf = "{cpf}"'
        cursor.execute(comando_sql)
        pacientes = cursor.fetchall()
        if pacientes:  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text="CPF já cadastrado!", font=fonte, fg="red")
        else:
            comando_sql = f"INSERT INTO pacientes (cpf, nome, telefone, endereco, cidade, estado, sexo, datanasc, estadocivil) VALUES ('{cpf}', '{nome}', '{telefone}', '{endereco}', '{cidade}', '{estado}', '{sexo}', '{datanasc}', '{estadocivil}')"
            cursor.execute(comando_sql)
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Paciente {nome} cadastrado!", font=fonte, fg="pink")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

# Função para cadastrar paciente

def cadastro_consultas():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de Consulta", font=ftitulo, fg=azulescuro, bg=bege)
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
    
    if codigo.strip() and data.strip() and hora.strip() and tipo and codpaciente.strip() and codmedico.strip() and codexame.strip():
        comando_sql = f'SELECT * FROM consultas WHERE codigo = "{codigo}"'
        cursor.execute(comando_sql)
        consultas = cursor.fetchall()

        if consultas:  # Verifica e cadastra se não existir
            resposta = tk.Label(janela, text="Código já cadastrado!", font=fonte, fg="red")
        else:  
            comando_sql = f'INSERT INTO consultas (codigo, data, hora, tipo, codpaciente, codmedico, codexame) VALUES ({codigo},"{data}","{hora}00","{tipo}",{codpaciente},{codmedico},{codexame})'
            cursor.execute(comando_sql)
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Consulta do código {codigo} cadastrado!", font=fonte, fg="pink")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)




def cadastro_medicos():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Cadastro de Médico", font=ftitulo, fg=azulescuro, bg=bege)
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
    
    if crm.strip() and nome and telefone.strip() and endereco and cidade and estado.strip() and especialidade:
        comando_sql = f'SELECT * FROM medicos WHERE crm = "{crm}"'
        cursor.execute(comando_sql)
        medicos = cursor.fetchall()
        if medicos:  # Verifica e cadastra se não existir
            comando_sql = f"INSERT INTO medicos (crm, nome, telefone, endereco, cidade, estado, especialidade) VALUES ('{crm}', '{nome}', '{telefone}', '{endereco}', '{cidade}', '{estado}', '{especialidade}')"
            cursor.execute(comando_sql)
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Médico {nome} cadastrado!", font=fonte, fg="pink")

        else:  # Se já existir
            resposta = tk.Label(janela, text="Médico já cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    
    resposta.pack(pady=20)

def alterar():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_alterar_e = tk.Button(janela, text="Alterar Exames", font=fonte, bg=azulclaro, fg="black", command=alteracao_exames)
    botao_alterar_e.pack(pady=10)

    botao_alterar_p = tk.Button(janela, text="Alterar Pacientes", font=fonte, bg=azulclaro, fg="black", command=alteracao_pacientes)
    botao_alterar_p.pack(pady=10)

    botao_alterar_c= tk.Button(janela, text="Alterar Consultas", font=fonte, bg=azulclaro, fg="black", command=alteracao_consultas)
    botao_alterar_c.pack(pady=10)

    botao_alterar_m= tk.Button(janela, text="Alterar Médicos", font=fonte, bg=azulclaro, fg="black", command=alteracao_medicos)
    botao_alterar_m.pack(pady=10) 

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def alteracao_exames():
    for widget in janela.winfo_children():
        widget.destroy()

    global resposta  
    if resposta is not None:
        resposta.destroy()  

    titulo = tk.Label(janela, text="Alteração de Exame", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    def next_entry(event, next_widget):
        next_widget.focus()

    codigo = tk.Label(janela, text="Código:", font=fonte)
    codigo.pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=fonte)
    entrada_codigo.pack(pady=5)

    preparo = tk.Label(janela, text="Preparo:", font=fonte)
    preparo.pack(pady=5)
    entrada_preparo = tk.Entry(janela, font=fonte)
    entrada_preparo.pack(pady=5)

    pos_exame = tk.Label(janela, text="Pós Exame:", font=fonte)
    pos_exame.pack(pady=5)
    entrada_pos_exame = tk.Entry(janela, font=fonte)
    entrada_pos_exame.pack(pady=5)

    entrada_codigo.bind("<Return>", lambda event: next_entry(event, entrada_preparo))
    entrada_preparo.bind("<Return>", lambda event: next_entry(event, entrada_pos_exame))
    entrada_pos_exame.bind("<Return>", lambda _: alterar_exames(
        entrada_codigo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: alterar_exames(
        entrada_codigo.get(),
        entrada_preparo.get(),
        entrada_pos_exame.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def alterar_exames(codigo, preparo, pos_exame):
    global resposta  
    if resposta is not None:
        resposta.destroy()

    if codigo.strip() and (preparo or pos_exame):
        comando_sql= f'SELECT codigo FROM exames WHERE codigo={codigo}'
        cursor.execute(comando_sql)
        exames=cursor.fetchall()
        if exames:           
            if preparo:
                comando_sql=f'UPDATE exames SET preparo="{preparo}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            if pos_exame:
                comando_sql=f'UPDATE exames SET pos_exame="{pos_exame}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)    
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Exame alterado!", font=fonte, fg="pink")    
        else:
            resposta = tk.Label(janela, text=f"Código não cadastrado!", font=fonte, fg="red")
    else:
        resposta=tk.Label(janela, text=f"Faltam informações!", font=fonte, fg="red")
    resposta.pack(pady=20)

def alteracao_pacientes():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Alteração de Paciente", font=ftitulo, fg=azulescuro, bg=bege)
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

    estadocivil = tk.Label(janela, text="Estado civil:", font=fonte)
    estadocivil.pack(pady=5)
    entrada_estadocivil = tk.Entry(janela, font=fonte)
    entrada_estadocivil.pack(pady=5)

    entrada_cpf.bind("<Return>", lambda event: next_entry(event, entrada_nome))
    entrada_nome.bind("<Return>", lambda event: next_entry(event, entrada_telefone))
    entrada_telefone.bind("<Return>", lambda event: next_entry(event, entrada_endereco))
    entrada_endereco.bind("<Return>", lambda event: next_entry(event, entrada_cidade))
    entrada_cidade.bind("<Return>", lambda event: next_entry(event, entrada_estado))
    entrada_estado.bind("<Return>", lambda event: next_entry(event, entrada_estadocivil))
    entrada_estadocivil.bind("<Return>", lambda _: alterar_pacientes(
        entrada_cpf.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_estadocivil.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: alterar_pacientes(
        entrada_cpf.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get(),
        entrada_estadocivil.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def alterar_pacientes(cpf, nome, telefone, endereco, cidade, estado, estadocivil):
    global resposta  
    if resposta is not None:
        resposta.destroy()

    if cpf.strip() and (nome or telefone or endereco or cidade or estado or estadocivil):
        comando_sql= f'SELECT cpf FROM pacientes WHERE cpf={cpf}'
        cursor.execute(comando_sql)
        pacientes=cursor.fetchall()
        if pacientes:
            if nome:
                comando_sql = f'UPDATE pacientes SET nome="{nome}" where cpf={cpf}'
                cursor.execute(comando_sql)
            if telefone:
                comando_sql = f'UPDATE pacientes SET telefone="{telefone}" where cpf={cpf}'
                cursor.execute(comando_sql)
            if endereco:
                comando_sql = f'UPDATE pacientes SET endereco="{endereco}" where cpf={cpf}'
                cursor.execute(comando_sql)
            if cidade:
                comando_sql = f'UPDATE pacientes SET cidade="{cidade}" where cpf={cpf}'
                cursor.execute(comando_sql)
            if estado:
                comando_sql = f'UPDATE pacientes SET estado="{estado}" where cpf={cpf}'
                cursor.execute(comando_sql)
            if estadocivil:
                comando_sql = f'UPDATE pacientes SET estadocivil="{estadocivil}" where cpf={cpf}'
                cursor.execute(comando_sql)
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Paciente alterado!", font=fonte, fg="pink")
        else:
            resposta = tk.Label(janela, text=f"CPF não cadastrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text=f"Faltam informações!", font=fonte, fg="red")
        
        resposta.pack(pady=20)

def alteracao_consultas():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Alteração de Consulta", font=ftitulo, fg=azulescuro, bg=bege)
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
    entrada_tipo.bind("<Return>", lambda event: next_entry(event, entrada_codmedico))
    entrada_codmedico.bind("<Return>", lambda event: next_entry(event, entrada_codexame))
    entrada_codexame.bind("<Return>", lambda event: alterar_consultas(     
     entrada_codigo.get(),
     entrada_data.get(),
     entrada_hora.get(),
     entrada_tipo.get(),
     entrada_codmedico.get(),
     entrada_codexame.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: alterar_consultas(
        entrada_codigo.get(),
        entrada_data.get(),
        entrada_hora.get(),
        entrada_tipo.get(),
        entrada_codmedico.get(),
        entrada_codexame.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def alterar_consultas(codigo, data, hora, tipo, codmedico, codexame):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if codigo.strip() and (data.strip() or hora.strip() or tipo or codmedico.strip() or codexame.strip()):
        comando_sql = f'SELECT * FROM consultas WHERE codigo = "{codigo}"'
        cursor.execute(comando_sql)
        consultas = cursor.fetchall()
        if consultas: 
            if data:
                comando_sql=f'UPDATE consultas SET data="{data}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            if hora:
                comando_sql=f'UPDATE consultas SET hora="{hora}00" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            if tipo:
                comando_sql=f'UPDATE consultas SET tipo="{tipo}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            if codmedico:
                comando_sql=f'UPDATE consultas SET codmedico="{codmedico}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            if codexame:
                comando_sql=f'UPDATE consultas SET codexame="{codexame}" WHERE codigo={codigo}'
                cursor.execute(comando_sql)
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Consulta alterada!", font=fonte, fg="pink")    
        else:
            resposta = tk.Label(janela, text=f"Código não cadastrado!", font=fonte, fg="red")
    else:
        resposta=tk.Label(janela, text=f"Faltam informações!", font=fonte, fg="red")
    resposta.pack(pady=20)

def alteracao_medicos():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Alteração de Médico", font=ftitulo, fg=azulescuro, bg=bege)
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

    entrada_crm.bind("<Return>", lambda event: next_entry(event, entrada_nome))
    entrada_nome.bind("<Return>", lambda event: next_entry(event, entrada_telefone))
    entrada_telefone.bind("<Return>", lambda event: next_entry(event, entrada_endereco))
    entrada_endereco.bind("<Return>", lambda event: next_entry(event, entrada_cidade))
    entrada_cidade.bind("<Return>", lambda event: next_entry(event, entrada_estado))
    entrada_estado.bind("<Return>", lambda _: alterar_medicos(
        entrada_crm.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get()
    ))

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: alterar_medicos(
        entrada_crm.get(),
        entrada_nome.get(),
        entrada_telefone.get(),
        entrada_endereco.get(),
        entrada_cidade.get(),
        entrada_estado.get()
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

# Envia os dados para o banco de dados
def alterar_medicos(crm, nome, telefone, endereco, cidade, estado):
    global resposta  
    if resposta is not None:
        resposta.destroy()  
    
    if crm.strip() and (nome or telefone.strip() or endereco or cidade or estado.strip()):
        comando_sql = f'SELECT * FROM medicos WHERE crm = "{crm}"'
        cursor.execute(comando_sql)
        medicos = cursor.fetchall()
        if medicos: 
            if nome:
                comando_sql=f'UPDATE medicos SET nome="{nome}" WHERE crm={crm}'
                cursor.execute(comando_sql)
            if telefone:
                comando_sql=f'UPDATE medicos SET telefone="{telefone}" WHERE crm={crm}'
                cursor.execute(comando_sql)    
            if endereco:
                comando_sql=f'UPDATE medicos SET endereco="{endereco}" WHERE crm={crm}'
                cursor.execute(comando_sql)    
            if cidade:
                comando_sql=f'UPDATE medicos SET cidade="{cidade}" WHERE crm={crm}'
                cursor.execute(comando_sql)    
            if estado:
                comando_sql=f'UPDATE medicos SET estado="{estado}" WHERE crm={crm}'
                cursor.execute(comando_sql)    
            conexao_banco.commit()
            resposta = tk.Label(janela, text=f"Médico alterado!", font=fonte, fg="pink")    
        else:
            resposta = tk.Label(janela, text=f"Código não cadastrado!", font=fonte, fg="red")
    else:
        resposta=tk.Label(janela, text=f"Faltam informações!", font=fonte, fg="red")
    resposta.pack(pady=20)

     
def excluir():
    for widget in janela.winfo_children():
        widget.destroy()

    titulo = tk.Label(janela, text="Exclusão de Consulta", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    codigo = tk.Label(janela, text="Código:", font=fonte)
    codigo.pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=fonte)
    entrada_codigo.pack(pady=5)

    botao_enviar = tk.Button(janela, text="Enviar", bg=azulclaro , font=fonte, 
    command=lambda: excluir_consultas(
        entrada_codigo.get(),
    ))
    botao_enviar.pack(pady=10)

    botao_voltar = tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=azulclaro)
    botao_voltar.pack(pady=5)

def excluir_consultas(codigo):
    global resposta, botao_sim
    if resposta is not None:
        resposta.destroy()

    if codigo.strip(): 
        comando_sql = f"SELECT * FROM consultas WHERE codigo = {codigo}"
        cursor.execute(comando_sql)
        consultas = cursor.fetchone()
        if consultas:
            data = consultas[1]  
            tipo = consultas[3]
            if botao_sim is not None:
                botao_sim.destroy()
            resposta = tk.Label(janela, text=f"Você tem certeza que deseja excluir a consulta que está agendada para {data}, do tipo {tipo}?", font=fonte, fg="blue")

            botao_sim = tk.Button(janela, text="Sim", font=fonte, bg="green", fg="white", command=lambda: confirmacao_exclusao(codigo))
            botao_sim.pack(pady=10)
        else:
            resposta = tk.Label(janela, text=f"Código não cadastrado!", fg="red", font=fonte)
    else:
        resposta = tk.Label(janela, text="Faltam informações!", fg="red", font=fonte)
    resposta.pack(pady=10)

def confirmacao_exclusao(codigo):
    global resposta
    if resposta is not None:
        resposta.destroy()

    comando_sql = f"DELETE FROM consultas WHERE codigo = {codigo}"
    cursor.execute(comando_sql)
    conexao_banco.commit()

    resposta=tk.Label(janela, text=f"Consulta {codigo} excluída com sucesso!", fg="green", font=fonte)
    resposta.pack(pady=10)
    botao_sim.destroy()

def visualizar():
    for widget in janela.winfo_children():  
        widget.destroy()

    titulo = tk.Label(janela, text="Hospital Ghellere Da Silva Machado", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    botao_visualizar_e = tk.Button(janela, text="Visualizar Exames", font=fonte, command=lambda: visualizacao("Exame", "codigo", "exames"))
    botao_visualizar_e.pack(pady=10)

    botao_visualizar_p = tk.Button(janela, text="Visualizar Pacientes", font=fonte, command=lambda: visualizacao("Paciente", "cpf", "pacientes"))
    botao_visualizar_p.pack(pady=10)

    botao_visualizar_c = tk.Button(janela, text="Visualizar Consultas", font=fonte, command=lambda: visualizacao("Consulta", "codigo", "consultas"))
    botao_visualizar_c.pack(pady=10)

    botao_visualizar_m = tk.Button(janela, text="Visualizar Médico", font=fonte, command=lambda: visualizacao("Médico", "crm", "medicos"))
    botao_visualizar_m.pack(pady=10)

def visualizacao(nome, campo, tabela):
    for widget in janela.winfo_children(): 
        widget.destroy()

    titulo = tk.Label(janela, text=f"Visualização de {nome}", font=ftitulo, fg=azulescuro, bg=bege)
    titulo.pack(pady=20)

    codigo = tk.Label(janela, text="Código:", font=fonte) 
    codigo.pack(pady=5)
    
    entrada_codigo = tk.Entry(janela, font=fonte) 
    entrada_codigo.pack(pady=5)

    def enviar():
        global resposta, infos
        for info in infos:
            info.destroy()
        infos.clear()
        if resposta is not None:
            resposta.destroy()

        codigo = entrada_codigo.get()   #pega o codigo
        
        if codigo.strip():  #ver se eh um numero msm
            comando_sql = f"SELECT * FROM {tabela} WHERE {campo} = {codigo}"
            cursor.execute(comando_sql)
            item = cursor.fetchone() #pega o primeiro item encontrado (codigo)
            #verifica o codigo
            if item:
                resposta = tk.Label(janela, text=f"Detalhes:", font=fonte, fg="blue")
                resposta.pack(pady=10)
                # pegando de cada tabela os itens e armazenando numa lista+tupla
                if tabela == 'medicos':
                    lista = [
                        ("CRM", item[0]),
                        ("Nome", item[1]),
                        ("Telefone", item[2]),
                        ("Endereço", item[3]),
                        ("Cidade", item[4]),
                        ("Estado", item[5]),
                        ("Especialidade", item[6]),
                    ]
                elif tabela == 'pacientes':
                    lista = [
                        ("CPF", item[0]),
                        ("Nome", item[1]),
                        ("Telefone", item[2]),
                        ("Endereço", item[3]),
                        ("Cidade", item[4]),
                        ("Estado", item[5]),
                        ("Sexo", item[6]),
                        ("Data de Nascimento", item[7]),
                        ("Estado Civil", item[8]),
                    ]
                elif tabela == 'exames':
                    lista = [
                        ("Código", item[0]),
                        ("Descrição", item[1]),
                        ("Tipo", item[2]),
                        ("Preparo", item[3] if item[3] else "Nenhum"),  #  else para campo vazio
                        ("Pós Exame", item[4] if item[4] else "Nenhum"),  # else para campo vazio
                    ]
                elif tabela == 'consultas':
                    lista = [
                        ("Código", item[0]),
                        ("Data", item[1]),
                        ("Hora", item[2]),
                        ("Tipo", item[3]),
                        ("Código Paciente", item[4]),
                        ("Código Médico", item[5]),
                        ("Código Exame", item[6]),
                    ]

                # Exibe as informações de cada campo
                for chave, valor in lista: #pega os bagulhos da lista
                    info = tk.Label(janela, text=f"{chave}: {valor}", font=fonte)
                    info.pack(pady=5) #esse label mostra os itens 
                    infos.append(info)

            else:
                resposta = tk.Label(janela, text=f"Não encontrado {tabela} com este código", fg="red", font=fonte)
        else:
            resposta = tk.Label(janela, text="Por favor, insira um código válido.", fg="red", font=fonte)
        resposta.pack(pady=10) 

    #botao enviar padrao
    enviar_botao = tk.Button(janela, text="Enviar", font=fonte, command=enviar)
    enviar_botao.pack(pady=10)

    voltar_botao = tk.Button(janela, text="Voltar", font=fonte, command=menu)
    voltar_botao.pack(pady=10)



menu()

janela.mainloop()

cursor.close()
conexao_banco.close()