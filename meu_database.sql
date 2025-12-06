CREATE TABLE aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_de_ingresso TIMESTAMP DEFAULT NOW()
);

CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INTEGER,
    valor_inscricao NUMERIC(10, 2) NOT NULL
);

CREATE TABLE matricula (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES aluno(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    data_de_matricula TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT "pendente"
);
