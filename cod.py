import mysql.connector
import tkinter as tk

conexaobanco=mysql.connector.connect (host="localhost", 
user="root", password='', database="hospital") #tupla
cursor=conexaobanco.cursor()

janela = tk.Tk()
janela.title("Exemplo Tkinter")



def validarnumero(char):  #ver se caracteres digitados sao numeros
    return char.isdigit() or char == ""
vnum = (janela.register(validarnumero), '%S')

def validartamanho(texto):  #ver se caracteres digitados sao menores ou iguais a 5
    return len(texto) <= 5
vtam = (janela.register(validartamanho), '%P')

def validarnumtam(char, texto):  #juncao das funcoes de numero e tamanho
    return validarnumero(char) and validartamanho(texto)
vnumtam= (janela.register(validarnumtam), '%S', '%P')

def cadmedico():
    def ver():
        sql=f'select * from medicos where crm="{crmget}"'
        cursor.execute(sql)
        dados=cursor.fetchone()
        print(dados)
        if dados:
            texto = tk.Label(janela, text="Médico já cadastrado com este crm!")
            texto.pack()
        else:
            texto = tk.Label(janela, text="Nome:")
            texto.pack()
            crm= tk.Entry(janela)
            crm.pack(pady=20)


    texto = tk.Label(janela, text="Cadastro do médico!")
    texto.pack()


    texto = tk.Label(janela, text="CRM:")
    texto.pack()
    crm= tk.Entry(janela, validate='key', validatecommand=vnumtam)
    crm.pack(pady=20)
    crmget = crm.get()
    print(crmget)
    enviar = tk.Button(janela, text='Enviar dados', command=ver)
    enviar.pack(pady=20)
    




def cad():
    medico = tk.Button(janela, text='Médico', command=cadmedico)
    medico.pack(pady=20)

"""     comandosql=f'select * from livros where titulo="{titulo}" and autor="{autor}"'
    cursor.execute(comandosql)
    livros=cursor.fetchone()

    if livros:
        print("Livro já cadastrado!")
    else:
        id=int(input('Digite a id do livro: '))
        anopub=int(input('Digite o ano de publicação do livro: '))

        comandosql=f'insert into livros (id,titulo,autor,anopublicacao, disponivel) values ({id}, "{titulo}", "{autor}", {anopub}, 1)'
        cursor.execute(comandosql)
        conexaobanco.commit()
        print("Livro cadastrado com sucesso!") """




cadastrar=tk.Button(janela, text='Cadastrar', command=cad)
cadastrar.pack(pady=20)


janela.mainloop()