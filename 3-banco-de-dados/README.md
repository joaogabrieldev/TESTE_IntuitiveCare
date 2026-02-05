# Etapa 3: Teste de Banco de Dados e Análise

## 🎯 Objetivo da Etapa

Esta etapa foca na persistência e análise dos dados processados nas etapas anteriores. Os objetivos principais são:
- Modelar um esquema de banco de dados relacional eficiente.
- Importar dados de múltiplas fontes (CSVs com diferentes encodings e formatos).
- Executar queries analíticas complexas para extrair insights de negócio.

## 🏗️ Arquitetura

### Estrutura do Projeto

```bash
3-banco-de-dados/ 
    ├── csv_files/ # Diretório contendo os CSVs gerados nas etapas 1 e 2 
    ├── carga_banco.py # Script Python para carga e orquestração (ETL) 
    ├── ddl_db.sql # Scripts de definição das tabelas (CREATE) 
    ├── queries_analiticas.sql # Queries de negócio complexas 
    ├── queries_db.sql # Queries de validação executadas pelo script 
    ├── intuitive_care.db # Banco de dados SQLite gerado 
    └── README.md # Documentação do projeto
```
### Design Pattern

Adotou-se uma abordagem **ELT (Extract, Load, Transform)** híbrida:
1.  **Extract**: Leitura dos CSVs via Pandas.
2.  **Transform (In-Memory)**: Normalização de nomes de colunas, conversão de tipagem e tratamento de nulos via Python.
3.  **Load**: Persistência no banco de dados relacional.
4.  **Analysis**: Transformações finais e agregações realizadas via SQL.

## 🔧 Decisões Técnicas

### 1. Modelagem de Dados (Normalização)

**Decisão**: Modelo Normalizado (Opção B).

**Justificativa**: Optei por separar os dados em tabelas distintas (operadoras_cadastral e detalhe_despesas) ligadas por Chave Estrangeira (REG_ANS). Essa abordagem normalizada reduz a redundância, economizando armazenamento ao evitar que dados cadastrais — como Razão Social, Cidade e UF — se repitam a cada linha de despesa. Além disso, o modelo assegura a integridade dos dados, garantindo que toda despesa esteja vinculada a uma operadora válida, e favorece a manutenibilidade, permitindo que atualizações cadastrais sejam realizadas em um único local.

### 2. Tipagem de Dados

**Decisão**: Uso de `DECIMAL` para moeda e `DATE` para datas.

**Justificativa**:
Quanto à tipagem de dados, o tipo DECIMAL(15,2) foi escolhido em detrimento de FLOAT para evitar erros de arredondamento em cálculos financeiros (floating point arithmetic errors), garantindo a precisão nos centavos. Já para o armazenamento temporal, o uso de DATE (ou formato ISO YYYY-MM-DD no SQLite) foi priorizado por permitir a ordenação cronológica correta e o uso eficiente de funções de data, como MONTH e STRFTIME, operações que seriam inviáveis performaticamente caso os dados fossem tratados como VARCHAR.

### 3. Estratégia de Carga (Python vs SQL Loader)

**Decisão**: Script Python (`carga_banco.py`) utilizando `Pandas` e `SQLAlchemy`.

**Justificativa**: A adoção de um script Python (carga_banco.py) em detrimento do carregamento direto via SQL (LOAD DATA INFILE) justifica-se pelas severas inconsistências presentes nos arquivos CSV de entrada, que atuariam como bloqueios técnicos em uma ingestão nativa. O script funciona como uma camada indispensável de sanitização, responsável por unificar o encoding misto dos arquivos — que oscilam entre latin1, utf-8 e utf-8-sig —, converter corretamente a formatação numérica do padrão brasileiro (vírgula decimal), frequentemente interpretada como texto pelos motores SQL, e normalizar headers inconsistentes que apresentam variações de nomenclatura e espaços em branco, assegurando a padronização dos dados antes da inserção no banco.

### 4. SQLite & MySQL 

**Decisão**: Desenvolvimento de scripts adaptados para dois ambientes: **SQLite** (para automação local) e **MySQL** (para conformidade com o enunciado).

**Justificativa**: Para priorizar a facilidade de execução ("Run") na máquina do avaliador, utilizei o SQLite no script de automação, pois ele dispensa a instalação de servidores de banco de dados complexos. Por conta disso, criei versões das queries otimizadas para a sintaxe do SQLite (ex: uso de strftime para datas) no arquivo de validação automática, enquanto mantive a lógica estrutural compatível com MySQL nos arquivos de definição, garantindo que o projeto seja "Plug and Play" sem ferir os requisitos originais de compatibilidade.

## 📊 Consultas Analíticas Desenvolvidas

### Query 1: Crescimento de Despesas
Identifica as 5 operadoras com maior crescimento percentual entre o primeiro e o último trimestre.
- **Desafio**: Lidar com operadoras sem dados em todos os períodos.
- **Solução**: Uso de CTEs (`WITH`) para calcular saldos trimestrais isolados e depois comparar o delta percentual apenas onde `Valor_Inicial > 0`.

### Query 2: Distribuição Geográfica (UF)
Lista os estados com maiores despesas e a média por operadora.
- **Abordagem**: `JOIN` entre tabela de fatos (despesas) e dimensão (cadastro).
- **Cálculo**: Agregação dupla - Soma total por UF e Média das Somas por Operadora.

### Query 3: Performance Consistente
Identifica operadoras acima da média de mercado em 2 ou mais trimestres.
- **Abordagem**: CTE's em Cascata.
- **Lógica**: Comparação trimestral entre despesa da operadora e média de mercado, filtrando por recorrência (≥ 2).

- **Justificativa**: A escolha por **CTEs (Common Table Expressions)** torna o código mais legível e linear, evitando a confusão de consultas aninhadas. Além de facilitar a manutenção ao centralizar as regras de tempo, essa abordagem melhora a performance: o banco calcula a média do mercado apenas uma vez por trimestre — e não linha por linha —, garantindo um processamento final muito mais eficiente.

## 📦 Dependências

### Bibliotecas Utilizadas

```python
pandas        # Leitura, limpeza e manipulação de CSVs
sqlalchemy    # ORM e conexão com Banco de Dados
```

### Instalação

```Bash
pip install pandas sqlalchemy
```

## 🚀 Como Executar

1. Certifique-se de que os arquivos CSV (`consolidado_despesas.csv`, `despesas_agregadas.csv`, `Relatorio_Cadop.csv`) estejam na pasta ou subpasta configurada no script.

2. Execute o script de carga:

```Bash
python carga_banco.py
```
#### O que o script fará:

1. Criará o banco de dados `intuitive_care.db` (SQLite).

2. Lerá os CSVs, tratará encodings e decimais.

3. Criará as tabelas e inserirá os dados.

4. Executará automaticamente as queries de validação (`queries_db.sql`) e exibirá os resultados no terminal.

## 📝 Notas Finais

### Este projeto demonstra:

- ✅ Modelagem de dados relacional (DDL).

- ✅ Manipulação robusta de dados com Python (ETL).

- ✅ Tratamento de erros de encoding e tipagem (Data Quality).

- ✅ Complexidade em SQL (Joins, Aggregations, CTEs).