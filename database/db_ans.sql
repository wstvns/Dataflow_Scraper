-- Criar tabela rol_procedimentos
CREATE TABLE rol_procedimentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50),
    descricao TEXT,
    odontologia BOOLEAN,
    ambulatorial BOOLEAN
);

-- Criar tabela operadoras
CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50) UNIQUE,
    cnpj VARCHAR(20),
    razao_social TEXT,
    modalidade VARCHAR(50),
    uf VARCHAR(5),
    data_registro DATE
);

-- Criar tabela demonstracoes_contabeis
CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50) REFERENCES operadoras(registro_ans),
    ano INT NOT NULL,
    trimestre INT NOT NULL,
    evento_sinistros NUMERIC(18,2) CHECK (evento_sinistros >= 0)
);

-- Importação corrigida para cada arquivo específico
COPY rol_procedimentos(codigo, descricao, odontologia, ambulatorial)
FROM 'database/data/Rol_de_Procedimentos.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

COPY operadoras(registro_ans, cnpj, razao_social, modalidade, uf, data_registro)
FROM 'database/data/Relatorio_cadop.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

COPY demonstracoes_contabeis(registro_ans, ano, trimestre, evento_sinistros)
FROM 'database/data/Demonstracoes_Contabeis.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

-- 10 operadoras com maiores despesas no último trimestre disponível
SELECT registro_ans, SUM(evento_sinistros) AS total_despesas
FROM demonstracoes_contabeis
WHERE (ano, trimestre) = (
    SELECT ano, MAX(trimestre)
    FROM demonstracoes_contabeis
    WHERE ano = (SELECT MAX(ano) FROM demonstracoes_contabeis)
)
GROUP BY registro_ans
ORDER BY total_despesas DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
SELECT registro_ans, SUM(evento_sinistros) AS total_despesas
FROM demonstracoes_contabeis
WHERE ano = (SELECT MAX(ano) FROM demonstracoes_contabeis)
GROUP BY registro_ans
ORDER BY total_despesas DESC
LIMIT 10;