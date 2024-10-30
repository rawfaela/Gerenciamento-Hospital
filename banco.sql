create DATABASE hospital;

create table medicos(
    crm int(5)  not null,
    nome varchar(50)  not null,
    endereco varchar(50) not null,
    telefone int(8) not null,
    cidade varchar(50) not null,
    estado varchar(50) not null,
    especialidade varchar(50) not null,
    primary key (crm)
);

create table medicamentos(
    codigo int(5) not null,
    nome varchar(50) not null,
    laboratorio varchar(50) not null,
    tipo varchar(50) not null,
    indicacao varchar(100) not null,
    efeito varchar(100) not null,
    primary key(codigo),
);

create table pacientes(
    cpf int(10) not null,
    nome varchar(50) not null,
    telefone int(8) not null,
    cidade varchar(50) not null,
    estado varchar(50) not null,
    sexo char(1) not null,
    datanasc date  not null,
    estadocivil varchar(50) not null,
    codmedicamento int(5),
    primary key (cpf),
    foreign key (codmedicamento) references medicamentos(codigo)
);

create table exames(
    codigo int(5) not null,
    descricao varchar(100) not null,
    tipo varchar(50) not null,
    preparo varchar(100),
    pos_exame varchar(100),
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
    foreign key (codpaciente) references pacientes(codigo),
    foreign key (codmedico) references medicos(crm),
    foreign key (codexame) references exames(codigo)
);