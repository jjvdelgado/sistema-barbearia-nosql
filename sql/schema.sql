CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    data_nascimento DATE,
    data_cadastro DATE DEFAULT CURRENT_DATE,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS barbeiro (
    id_barbeiro SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    data_contratacao DATE DEFAULT CURRENT_DATE,
    especialidade VARCHAR(50),
    comissao_percentual DECIMAL(5,2) DEFAULT 30.00,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    duracao_estimada INTEGER NOT NULL, 
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco_venda DECIMAL(10,2) NOT NULL,
    estoque_atual INTEGER DEFAULT 0,
    estoque_minimo INTEGER DEFAULT 5,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS atendimento (
    id_atendimento SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_barbeiro INTEGER NOT NULL,
    tipo VARCHAR(20) DEFAULT 'walkin', -- 'agendado' ou 'walkin'
    data_agendada DATE, -- Para atendimentos agendados
    horario_agendado TIME, -- Para atendimentos agendados
    data_atendimento DATE DEFAULT CURRENT_DATE,
    horario_inicio TIME,
    horario_fim TIME,
    status VARCHAR(20) DEFAULT 'agendado', 
    valor_total DECIMAL(10,2),
    forma_pagamento VARCHAR(20),
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE RESTRICT,
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiro(id_barbeiro) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS atendimento_servico (
    id_atendimento INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    preco_cobrado DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_atendimento, id_servico),
    FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS venda_produto (
    id_venda SERIAL PRIMARY KEY,
    id_atendimento INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS horario_trabalho (
    id_horario SERIAL PRIMARY KEY,
    id_barbeiro INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiro(id_barbeiro) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_cliente_cpf ON cliente(cpf);
CREATE INDEX IF NOT EXISTS idx_barbeiro_cpf ON barbeiro(cpf);
CREATE INDEX IF NOT EXISTS idx_atendimento_data ON atendimento(data_atendimento);
CREATE INDEX IF NOT EXISTS idx_atendimento_agendado ON atendimento(data_agendada) WHERE data_agendada IS NOT NULL;