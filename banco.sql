--MUDAR TODOS OS MÁXIMOS PRA 500

create DATABASE hospital;

create table medicos(
    crm int(5)  not null,
    nome varchar(50)  not null,
    telefone int(8) not null,
    endereco varchar(50) not null,
    cidade varchar(50) not null,
    estado char(2) not null,
    especialidade varchar(50) not null,
    primary key (crm)
);

create table pacientes(
    cpf int(10) not null,
    nome varchar(50) not null,
    telefone int(8) not null,
    endereco varchar(50) not null,
    cidade varchar(50) not null,
    estado char(2) not null,
    sexo char(1) not null,
    datanasc date  not null,
    estadocivil varchar(50) not null,
    primary key (cpf)
);

create table exames(
    codigo int(5) not null,
    descricao varchar(100) not null,
    tipo varchar(50) not null,
    preparo varchar(150),
    pos_exame varchar(150),
    primary key (codigo)
);

create table consultas(
    codigo int(5) not null,
    data date not null,
    hora time  not null,
    tipo varchar(50) not null,
    codpaciente int(5) not null,
    codmedico int(5) not null,
    codexame int(5) not null,
    primary key (codigo),
    foreign key (codpaciente) references pacientes(cpf),
    foreign key (codmedico) references medicos(crm),
    foreign key (codexame) references exames(codigo)
);
