import mysql.connector
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

conexao_banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hospital"
)
cursor = conexao_banco.cursor()

bege = '#DDCCBB'
ciano = '#0087A0'
azul = '#336182'

janela = tk.Tk()
janela.state("zoomed")
janela.configure(background=bege)

imagem = Image.open("logo2.png")
imagem = imagem.resize((370, 278))
foto = ImageTk.PhotoImage(imagem)

fonte = font.Font(family="Arial", size=20)
ftitulo = font.Font(family="Arial", size=25, weight="bold")

resposta = None  
botao_sim = None 

def limitar_entrada(valor, campo):
    if valor == "":  
        return True

    elif campo in ('codigo', 'crm', 'codpaciente', 'codmedico', 'codexame'):
        if valor.isdigit(): 
            return True
        return False

    elif campo in ('cpf', 'telefone'):
        if valor.isdigit() and len(valor) <= 11:
            return True
        return False

    elif campo in ('datanasc', 'data'):
        if valor.isdigit() and len(valor) <= 8:
            return True  
        return False

    elif campo == 'estado':
        if valor.isalpha() and len(valor) <= 2: 
            return True
        return False
    
    elif campo in ('cidade','nome','especialidade'):
        if valor.isalpha() or " " in valor:
            return True
        return False

    elif campo in ('sexo', 'estadocivil'):
        if valor.isalpha():
            return True
        return False

    elif campo == 'hora':
        if (valor.isdigit() or ':' in valor) and len(valor) <= 5:  
            return True
        return False

    return True

def menu():
    for widget in janela.winfo_children():
        widget.destroy()
        
    label_imagem = tk.Label(janela, image=foto, bg=bege)
    label_imagem.pack()

    tk.Button(janela, text="Cadastrar", font=fonte, bg=ciano, fg="black", command=cadastrar).pack(pady=10)   

    tk.Button(janela, text="Alterar", font=fonte, bg=ciano, fg="black", command=alterar).pack(pady=10) 

    tk.Button(janela, text="Excluir", font=fonte, bg=ciano, fg="black", command=excluir).pack(pady=10)  

    tk.Button(janela, text="Visualizar", font=fonte, bg=ciano, fg="black", command=visualizar).pack(pady=10) 

def cadastrar():
    for widget in janela.winfo_children():
        widget.destroy()
        
    label_imagem = tk.Label(janela, image=foto, bg=bege)
    label_imagem.pack()

    tk.Button(janela, text="Cadastrar Exames", font=fonte, bg=ciano, fg="black", command=lambda: cadastro("Exame", [("codigo", "Código"), ("descricao", "Descrição"), ("tipo", "Tipo"), ("preparo", "Preparo"), ("pos_exame", "Pós Exame")], "exames")).pack(pady=10)

    tk.Button(janela, text="Cadastrar Pacientes", font=fonte, bg=ciano, fg="black", command=lambda: cadastro("Paciente", [("cpf", "CPF"), ("nome", "Nome"), ("telefone", "Telefone"), ("endereco", "Endereço"), ("cidade", "Cidade"), ("estado", "Estado"), ("sexo", "Sexo"), ("datanasc", "Data de nascimento"), ("estadocivil", "Estado Civil")], "pacientes")).pack(pady=10)

    tk.Button(janela, text="Cadastrar Consultas", font=fonte, bg=ciano, fg="black", command=lambda: cadastro("Consulta", [("codigo", "Código"), ("tipo", "Tipo"), ("data", "Data"), ("hora", "Hora"), ("codpaciente", "CPF do paciente"), ("codmedico", "CRM do médico"), ("codexame", "Código do exame")], "consultas")).pack(pady=10)

    tk.Button(janela, text="Cadastrar Médicos", font=fonte, bg=ciano, fg="black", command=lambda: cadastro("Médico", [("crm","CRM"),("nome","Nome"),("telefone","Telefone"), ("endereco","Endereço"),("cidade","Cidade"),("estado","Estado"), ("especialidade", "Especialidade")], "medicos")).pack(pady=10)    

    tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=ciano).pack(pady=5)


def cadastro(nome, campos, tabela):
    for widget in janela.winfo_children():
        widget.destroy()
        
    global resposta
    if resposta:
        resposta.destroy()

    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(2, weight=1) 

    tk.Label(janela, text=f"Cadastro de {nome}", font=ftitulo, fg=azul, bg=bege).grid(row=0, column=1, pady=50, padx=150)

    entradas = {}

    def next_entry(event, next_widget):
        next_widget.focus()

    for i, (campo_tabela, campo_nome) in enumerate(campos):
        tk.Label(janela, text=f"{campo_nome}:", font=fonte).grid(row=i+1, column=0, sticky='e', padx=10, pady=15)   
    
        validar = janela.register(limitar_entrada)

        entrada = tk.Entry(janela, font=fonte, validate="key", validatecommand=(validar, '%P', campo_tabela))
        entrada.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
        entradas[campo_tabela] = entrada

        if i < len(campos) - 1:
            entrada.bind("<Return>", lambda event, next_widget=campos[i + 1][0]: next_entry(event, entradas[next_widget]))
        else:
            entrada.bind("<Return>", lambda _: enviar_cadastro(nome, tabela, campos, entradas))

    tk.Button(janela, text="Enviar", bg=ciano, font=fonte, command=lambda: enviar_cadastro(nome, tabela, campos, entradas)).grid(row=len(campos)+1, column=1, pady=10)
    tk.Button(janela, text="Voltar", font=fonte, command=cadastrar, bg=ciano).grid(row=len(campos)+2, column=1, pady=10)

def enviar_cadastro(nome, tabela, campos, entradas):
    global resposta
    if resposta:
        resposta.destroy()

    erro = False

    valores = {campo: entradas[campo].get().strip() for campo, _ in campos}

    if all(valores[campo] for campo in valores): 
        codigo = campos[0][0]
        comando_sql = f'SELECT * FROM {tabela} WHERE {codigo} = "{valores[codigo]}"'
        cursor.execute(comando_sql)
        resultado = cursor.fetchall()

        if resultado:
            resposta = tk.Label(janela, text="Código já cadastrado!", font=fonte, fg="red")
        else:
            if resposta:
                resposta.destroy()

            if tabela != 'consultas':
                enviar_cadastrar(nome, tabela, valores, campos)
            else:
                cursor.execute(f'SELECT * FROM pacientes where cpf={valores[campos[4][0]]}')
                checar = cursor.fetchone()
                if checar is None:
                    resposta = tk.Label(janela, text=f"Código do paciente não encontrado!", font=fonte, fg="red")
                    resposta.grid(row=len(campos)+3, column=1, pady=10)
                    erro = True

                cursor.execute(f'SELECT * FROM medicos where crm={valores[campos[5][0]]}')
                checar = cursor.fetchone()
                if checar is None:
                    resposta = tk.Label(janela, text=f"Código do médico não encontrado!", font=fonte, fg="red")
                    resposta.grid(row=len(campos)+3, column=1, pady=10)
                    erro = True

                cursor.execute(f'SELECT * FROM exames where codigo={valores[campos[6][0]]}')
                checar = cursor.fetchone()
                if checar is None:                        
                    resposta = tk.Label(janela, text=f"Código do exame não encontrado!", font=fonte, fg="red")
                    resposta.grid(row=len(campos)+3, column=1, pady=10)
                    erro = True
                if erro:
                    return
                else:
                    enviar_cadastrar(nome, tabela, valores, campos)
    else:
        resposta = tk.Label(janela, text="Todos os campos devem ser preenchidos!", font=fonte, fg="red")
    resposta.grid(row=len(campos)+3, column=1, pady=10)
    
def enviar_cadastrar(nome, tabela, valores, campos):
    comando_sql = f"INSERT INTO {tabela} ({', '.join([campo for campo, _ in campos])}) VALUES ({', '.join([repr(valores[campo]) for campo, _ in campos])})"
    cursor.execute(comando_sql)
    conexao_banco.commit()
    
    descricao = valores[campos[1][0]]
    resposta = tk.Label(janela, text=f"{nome} {descricao} cadastrado!", font=fonte, fg="green")
    resposta.grid(row=len(campos)+3, column=1, pady=10)

def alterar():
    for widget in janela.winfo_children():
        widget.destroy()

    label_imagem = tk.Label(janela, image=foto, bg=bege)
    label_imagem.pack()

    tk.Button(janela, text="Alterar Exames", font=fonte, bg=ciano, fg="black", command=lambda: alteracao("Exame", [("codigo", "Código"), ("preparo", "Preparo"), ("pos_exame", "Pós Exame")], "exames")).pack(pady=10)

    tk.Button(janela, text="Alterar Pacientes", font=fonte, bg=ciano, fg="black", command=lambda: alteracao("Paciente", [("cpf", "CPF"), ("nome", "Nome"), ("telefone", "Telefone"), ("endereco", "Endereço"), ("cidade", "Cidade"), ("estado", "Estado"), ("estadocivil", "Estado Civil")], "pacientes")).pack(pady=10)

    tk.Button(janela, text="Alterar Consultas", font=fonte, bg=ciano, fg="black", command=lambda: alteracao("Consulta", [("codigo", "Código"), ("data", "Data"), ("hora", "Hora"), ("tipo", "Tipo"), ("codmedico", "CRM do médico"), ("codexame", "Código do exame")], "consultas")).pack(pady=10)

    tk.Button(janela, text="Alterar Médicos", font=fonte, bg=ciano, fg="black", command=lambda: alteracao("Médico", [("crm","CRM"),("nome","Nome"),("telefone","Telefone"), ("endereco","Endereço"),("cidade","Cidade"),("estado","Estado")], "medicos")).pack(pady=10) 

    tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=ciano).pack(pady=5)

def alteracao(nome, campos, tabela):
    for widget in janela.winfo_children():
        widget.destroy()
        
    global resposta
    if resposta:
        resposta.destroy()

    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(2, weight=1) 

    tk.Label(janela, text=f"Alteração de {nome}", font=ftitulo, fg=azul, bg=bege).grid(row=0, column=0, columnspan=5, pady=60, padx=150)

    entradas = {}

    def next_entry(event, next_widget):
        next_widget.focus()

    for i, (campo_tabela, campo_nome) in enumerate(campos):
        tk.Label(janela, text=f"{campo_nome}:", font=fonte).grid(row=i+1, column=0, sticky='e', padx=10, pady=15)

        validar = janela.register(limitar_entrada)
        entrada = tk.Entry(janela, font=fonte, validate="key", validatecommand=(validar, '%P', campo_tabela))
        entrada.grid(row=i+1, column=1, padx=10, pady=5) 
        entradas[campo_tabela] = entrada
        
        if i < len(campos) - 1:
            entrada.bind("<Return>", lambda event, next_widget=campos[i + 1][0]: next_entry(event, entradas[next_widget]))
        else:
            entrada.bind("<Return>", lambda _: enviar_alterar(nome, tabela, campos, entradas))

    tk.Button(janela, text="Enviar", bg=ciano, font=fonte, command=lambda: enviar_alterar(nome, tabela, campos, entradas)).grid(row=len(campos) + 1, column=0, columnspan=5, pady=10)
    tk.Button(janela, text="Voltar", font=fonte, command=alterar, bg=ciano).grid(row=len(campos) + 2, column=0, columnspan=5, pady=10)

def enviar_alterar(nome, tabela, campos, entradas):
    global resposta
    if resposta:
        resposta.destroy()

    erro = False

    valores = {campo: entradas[campo].get().strip() for campo, _ in campos}
    codigo = campos[0][0]

    if valores[codigo] and any(valores[campo] for campo in valores if campo != codigo and valores[campo]):
        cursor.execute(f'SELECT {codigo} FROM {tabela} WHERE {codigo}={valores[codigo]}')
        resultado = cursor.fetchone()

        if resultado:
            if tabela != 'consultas':
                enviar_alteracao(nome, tabela, valores, codigo, campos)
            else:
                if resposta:
                    resposta.destroy()

                if valores[campos[4][0]]:
                    cursor.execute(f'SELECT * FROM medicos where crm={valores[campos[4][0]]}')
                    checar = cursor.fetchone()
                    if checar is None:
                        resposta = tk.Label(janela, text=f"Código do médico não encontrado!", font=fonte, fg="red")
                        resposta.grid(row=len(campos) + 3, column=0, columnspan=5, pady=10)
                        erro = True

                if valores[campos[5][0]]:
                    cursor.execute(f'SELECT * FROM exames where codigo={valores[campos[5][0]]}')
                    checar = cursor.fetchone()
                    if checar is None:                        
                        resposta = tk.Label(janela, text=f"Código do exame não encontrado!", font=fonte, fg="red")
                        resposta.grid(row=len(campos) + 3, column=0, columnspan=5, pady=10)
                        erro = True
                if erro:
                    return
                else:
                    enviar_alteracao(nome, tabela, valores, codigo, campos)
        else:
            resposta = tk.Label(janela, text=f"Código não encontrado!", font=fonte, fg="red")
    else:
        resposta = tk.Label(janela, text="Faltam informações!", font=fonte, fg="red")

    resposta.grid(row=len(campos) + 3, column=0, columnspan=5, pady=10)

def enviar_alteracao(nome, tabela, valores, codigo, campos):
    global resposta
    if resposta:
        resposta.destroy()
    for campo, valor in valores.items():
        if valor and campo != codigo:
            cursor.execute(f'UPDATE {tabela} SET {campo}="{valor}" WHERE {codigo}={valores[codigo]}')
    conexao_banco.commit()
    resposta = tk.Label(janela, text=f"{nome} alterado com sucesso!", font=fonte, fg="green")
    resposta.grid(row=len(campos) + 3, column=0, columnspan=5, pady=10)
     
def excluir():
    for widget in janela.winfo_children():
        widget.destroy()

    validar = janela.register(limitar_entrada)

    tk.Label(janela, text="Exclusão de Consulta", font=ftitulo, fg=azul, bg=bege).pack(pady=20)

    tk.Label(janela, text="Código:", font=fonte).pack(pady=5)
    entrada_codigo = tk.Entry(janela, font=fonte, validate="key", validatecommand=(validar, '%P', "codigo"))
    entrada_codigo.pack(pady=5)

    entrada_codigo.bind("<Return>", lambda _: excluir_consultas(entrada_codigo.get()))

    tk.Button(janela, text="Enviar", bg=ciano , font=fonte, 
    command=lambda: excluir_consultas(
        entrada_codigo.get(),
    )).pack(pady=10)

    tk.Button(janela, text="Voltar", font=fonte, command=menu, bg=ciano).pack(pady=5)

def excluir_consultas(codigo):
    global resposta, botao_sim
    if resposta is not None:
        resposta.destroy()

    if codigo.strip(): 
        comando_sql = f"SELECT * FROM consultas WHERE codigo = {codigo}"
        cursor.execute(comando_sql)
        consultas = cursor.fetchone()
        if consultas:
            data = consultas[2]  
            tipo = consultas[1]
            if botao_sim is not None:
                botao_sim.destroy()
            resposta = tk.Label(janela, text=f"Você tem certeza que deseja excluir a consulta que está agendada para {data} do tipo {tipo}?", font=fonte, fg="blue")

            botao_sim = tk.Button(janela, text="Sim", font=fonte, bg="green", fg="white", command=lambda: confirmacao_exclusao(codigo))
            botao_sim.pack(pady=10)
        else:
            resposta = tk.Label(janela, text=f"Código não cadastrado!", fg="red", font=fonte)
    else:
        resposta = tk.Label(janela, text="Faltam informações!", fg="red", font=fonte)
    resposta.pack(pady=10)

def confirmacao_exclusao(codigo):
    global resposta, botao_sim
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
        
    label_imagem = tk.Label(janela, image=foto, bg=bege)
    label_imagem.pack()

    tk.Button(janela, bg=ciano, text="Visualizar Exames", font=fonte, command=lambda: visualizacao("Exame", "codigo", "exames", "Código")).pack(pady=10)

    tk.Button(janela, bg=ciano, text="Visualizar Pacientes", font=fonte, command=lambda: visualizacao("Paciente", "cpf", "pacientes", "CPF")).pack(pady=10)

    tk.Button(janela, bg=ciano, text="Visualizar Consultas", font=fonte, command=lambda: visualizacao("Consulta", "codigo", "consultas", "Código")).pack(pady=10)

    tk.Button(janela, bg=ciano, text="Visualizar Médico", font=fonte, command=lambda: visualizacao("Médico", "crm", "medicos", "CRM")).pack(pady=10)
    
    tk.Button(janela, text="Voltar", font=fonte, bg=ciano, command=menu).pack(pady=10)

def visualizacao(nome, campo, tabela, codigo):
    for widget in janela.winfo_children(): 
        widget.destroy()

    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(2, weight=1)

    validar = janela.register(limitar_entrada)

    tk.Label(janela, text=f"Visualização de {nome}", font=ftitulo, fg=azul, bg=bege).grid(row=0, column=0, columnspan=5, pady=60)

    tk.Label(janela, text=f"{codigo}:", font=fonte).grid(row=1, column=0, sticky='e', pady=15)   
    entrada_codigo = tk.Entry(janela, font=fonte, validate="key", validatecommand=(validar, '%P', campo))
    entrada_codigo.grid(row=1, column=1, padx=10, pady=5, sticky='we')

    infos=[]

    def enviar():
        global resposta
        for info in infos:
            info.destroy()
        infos.clear()
        if resposta is not None:
            resposta.destroy()

        codigo = entrada_codigo.get()  
        
        if codigo.strip():
            comando_sql = f"SELECT * FROM {tabela} WHERE {campo} = {codigo}"
            cursor.execute(comando_sql)
            item = cursor.fetchone()
            if item:
                resposta = tk.Label(janela, text=f"Detalhes:", font=fonte, fg="blue").grid(row=4, column=0, columnspan=5, pady=10, padx=50)
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
                        ("Preparo", item[3] if item[3] else "Nenhum"), 
                        ("Pós Exame", item[4] if item[4] else "Nenhum"), 
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
                for i, (chave, valor) in enumerate(lista):
                    info = tk.Label(janela, text=f"{chave}: {valor}", font=fonte)
                    info.grid(row=i+5, column=0, columnspan=5, pady=10, padx=50) 
                    infos.append(info)
            else:
                resposta = tk.Label(janela, text=f"Não encontrado {tabela} com este código", fg="red", font=fonte)
                resposta.grid(row=4, column=0, columnspan=5, pady=10, padx=50)
        else:
            resposta = tk.Label(janela, text="Por favor, insira um código válido.", fg="red", font=fonte)
            resposta.grid(row=4, column=0, columnspan=5, pady=10, padx=50)

    entrada_codigo.bind("<Return>", lambda _: enviar())

    tk.Button(janela, text="Enviar", font=fonte, command=enviar, bg=ciano).grid(row=2, column=0, columnspan=5, pady=10)

    tk.Button(janela, text="Voltar", font=fonte, command=visualizar, bg=ciano).grid(row=3, column=0, columnspan=5, pady=10)

menu()
janela.mainloop()
