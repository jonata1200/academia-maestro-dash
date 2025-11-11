-- Criação da tabela de Instrumentos
CREATE TABLE IF NOT EXISTS instrumentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_instrumento TEXT NOT NULL UNIQUE
);

-- Criação da tabela de Alunos
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento DATE,
    genero TEXT,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Ativo' -- Ativo, Inativo, Suspenso
);

-- Criação da tabela de Professores
CREATE TABLE IF NOT EXISTS professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT,
    data_contratacao DATE DEFAULT CURRENT_DATE,
    especializacao TEXT, -- Ex: "Violão Clássico", "Bateria Jazz"
    status TEXT DEFAULT 'Ativo' -- Ativo, Inativo
);

-- Tabela para mapear quais instrumentos cada professor leciona
CREATE TABLE IF NOT EXISTS professores_instrumentos (
    professor_id INTEGER,
    instrumento_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES professores(id),
    FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id),
    PRIMARY KEY (professor_id, instrumento_id)
);

-- Criação da tabela de Aulas Ofertadas (tipos de aulas)
CREATE TABLE IF NOT EXISTS aulas_ofertadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_aula TEXT NOT NULL UNIQUE, -- Ex: "Aula de Violão", "Aula de Teclado"
    instrumento_id INTEGER NOT NULL,
    FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id)
);

-- Criação da tabela de Matrículas (aluno se matricula em um tipo de aula)
CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    aula_ofertada_id INTEGER NOT NULL,
    data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fim_matricula DATE, -- Opcional, se houver pacotes com validade
    status TEXT DEFAULT 'Ativa', -- Ativa, Suspensa, Cancelada, Concluída
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (aula_ofertada_id) REFERENCES aulas_ofertadas(id)
);

-- Criação da tabela de Agenda de Aulas (aulas individuais agendadas)
CREATE TABLE IF NOT EXISTS agenda_aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    professor_id INTEGER NOT NULL,
    instrumento_id INTEGER NOT NULL, -- Para garantir que o instrumento da aula agendada está correto
    data_aula DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    valor_aula REAL NOT NULL DEFAULT 250.00, -- O valor da aula individual
    status TEXT DEFAULT 'Agendada', -- Agendada, Concluída, Cancelada, Remarcada
    observacoes TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (professor_id) REFERENCES professores(id),
    FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id),
    UNIQUE(professor_id, data_aula, hora_inicio) -- Garante que um professor não tenha aulas duplicadas no mesmo horário
);

-- Criação da tabela de Pagamentos
CREATE TABLE IF NOT EXISTS pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_pago REAL NOT NULL,
    metodo_pagamento TEXT, -- Cartão, Pix, Dinheiro, Boleto
    referencia_aula_id INTEGER, -- Chave estrangeira para agenda_aulas.id (se for pagamento de uma única aula)
    status TEXT DEFAULT 'Pago', -- Pago, Pendente, Cancelado, Estornado
    observacoes TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (referencia_aula_id) REFERENCES agenda_aulas(id)
);

-- Tabela para guardar configurações gerais, como o preço padrão da aula
CREATE TABLE IF NOT EXISTS configuracoes (
    chave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);