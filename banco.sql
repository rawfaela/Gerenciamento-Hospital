create DATABASE hospital;

create table medicos(
    crm                 int(5)         not null,
    nome                varchar(500)   not null,
    telefone            int(11)        not null,
    endereco            varchar(500)   not null,
    cidade              varchar(500)   not null,
    estado              char(2)        not null,
    especialidade       varchar(500)   not null,
    primary key (crm)
);


create table pacientes(
    cpf                 int(11)        not null,
    nome                varchar(500)   not null,
    telefone            int(11)        not null,
    endereco            varchar(500)   not null,
    cidade              varchar(500)   not null,
    estado              char(2)        not null,
    sexo                char(1)        not null,
    datanasc            date           not null,
    estadocivil         varchar(500)   not null,
    primary key (cpf)
);

create table exames(
    codigo              int(5)         not null,
    descricao           varchar(500)   not null,
    tipo                varchar(500)   not null,
    preparo             varchar(500),
    pos_exame           varchar(500),
    primary key (codigo)
);

create table consultas(
    codigo              int(5)         not null,
    tipo                varchar(500)   not null,
    data                date           not null,
    hora                time           not null,
    codpaciente         int(5)         not null,
    codmedico           int(5)         not null,
    codexame            int(5)         not null,
    primary key (codigo),
    foreign key (codpaciente) references pacientes(cpf),
    foreign key (codmedico) references medicos(crm),
    foreign key (codexame) references exames(codigo)
);
