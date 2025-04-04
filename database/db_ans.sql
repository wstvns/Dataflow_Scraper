-- Cria tabela dos dados do anexo 1
CREATE TABLE rol_procedimentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50),
    descricao TEXT,
    odontologia BOOLEAN,
    ambulatorial BOOLEAN
);

-- Cria tabela dos dados das operadoras
CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50),
    cnpj VARCHAR(20),
    razao_social TEXT,
    modalidade VARCHAR(50),
    uf VARCHAR(5),
    data_registro DATE
);

-- Cria tabela para armazenamento contabil
CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50),
    ano INT,
    trimestre INT,
    evento_sinistros NUMERIC(18,2)
);

-- Importa dados para a tabela do rol de procedimentos
COPY rol_procedimentos(codigo, descricao, odontologia, ambulatorial)
FROM 'database/data/Relatorio_cadop.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

-- Importar dados para a tabela operadoras
COPY operadoras(registro_ans, cnpj, razao_social, modalidade, uf, data_registro)
FROM 'database/data/Relatorio_cadop.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

-- Importar dados para a tabela demonstracoes contabeis
COPY demonstracoes_contabeis(registro_ans, ano, trimestre, evento_sinistros)
FROM 'database/data/Relatorio_cadop.csv'
DELIMITER ','
CSV HEADER ENCODING 'UTF8';

-- Query das 10 oepradoras com maiores despesas em sinistros
SELECT registro_ans, SUM(evento_sinistros) AS total_despesas
FROM demonstracoes_contabeis
WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE) 
AND trimestre = (SELECT MAX(trimestre) FROM demonstracoes_contabeis WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE))
GROUP BY registro_ans
ORDER BY total_despesas DESC
LIMIT 10;

-- Query do ultimo ano
SELECT registro_ans, SUM(evento_sinistros) AS total_despesas
FROM demonstracoes_contabeis
WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE) - 1
GROUP BY registro_ans
ORDER BY total_despesas DESC
LIMIT 10;
