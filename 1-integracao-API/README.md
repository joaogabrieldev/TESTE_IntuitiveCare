# Etapa 1: Integração de API - ETL de Dados ANS


## 🎯 Objetivo da Etapa

Desenvolver uma solução robusta para:
- Extrair dados trimestrais de demonstrações contábeis da ANS via API pública
- Transformar e padronizar os dados coletados
- Carregar os dados consolidados em formato CSV (local) ou S3 (cloud)

## 🏗️ Arquitetura

### Estrutura do Projeto

```
1-integração-API/
├── etl_ans.py          # Implementação ETL local (sem cloud)
├── etl_aws_demo.py     # Demonstração de Implementação ETL com AWS (serverless)
├── test_etl.py         # Testes unitários
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Documentação do projeto
```

### Design Pattern

Nesta etapa, utilizei o padrão **Classe Orientada a Objetos** com separação clara de responsabilidades:

- **`ETLEventsANS`**: Classe principal que encapsula toda a lógica ETL
- **`extract_and_transform()`**: Responsável pela extração e transformação dos dados
- **`load()` / `load_to_s3()`**: Responsável pelo carregamento dos dados processados
- **`implement()`**: Orquestra todo o processo ETL

## 🔧 Decisões Técnicas

### 1. Estruturação do Código

**Decisão**: Utilização de classe única com métodos bem definidos

**Justificativa**: A arquitetura orientada a objetos com classe única centraliza a lógica ETL, facilitando manutenção e correção de bugs. A estruturação em métodos bem definidos cria separação clara de responsabilidades (princípio SOLID). A mesma classe é reutilizada nas versões local e cloud (princípio DRY), garantindo consistência. A estrutura também facilita testes unitários isolados e melhora a legibilidade através de métodos auto-documentados.

### 2. Tratamento de Encoding

**Decisão**: Tentativa múltipla de encoding (latin1 → utf-8-sig)

**Justificativa**: Considerando que bases de dados governamentais, como as da ANS, frequentemente apresentam inconsistências de codificação (variando entre o padrão legado Windows-1252/Latin1 e o moderno UTF-8), implementei um mecanismo de leitura robusto. A estratégia prioriza o formato latin1 para cobrir a maioria dos arquivos históricos gerados por Excel, mas utiliza um fallback automático para utf-8-sig, assegurando que arquivos mais recentes ou convertidos sejam processados corretamente, o que garante a alta resiliência do pipeline de dados.

```python
try:
    df = pd.read_csv(f, sep=";", encoding="latin1", dtype=str)
except Exception:
    f.seek(0)
    df = pd.read_csv(f, sep=";", encoding="utf-8", dtype=str)
```

### 3. Normalização de Colunas

**Decisão**: Padronização de nomes de colunas (strip + uppercase)

**Justificativa**: Arquivos da ANS de diferentes trimestres podem apresentar variações críticas nos nomes de colunas (capitalização, espaçamento), causando erros em merge e análise. Para garantir a integridade e facilitar futuras consultas SQL, padronizei os nomes das colunas removendo espaços acidentais (`.strip()`) e convertendo-os para caixa alta (`.upper()`), o que previne erros comuns de diferenciação de caracteres. Simultaneamente, assegurei a rastreabilidade (Lineage) dos dados através da inclusão da coluna `TRIMESTRE_REF`, fornecendo o contexto temporal indispensável para distinguir a origem de cada registro dentro do arquivo consolidado e viabilizar análises cronológicas precisas.

### 4. Estratégia de Extração e Processamento em Memória

**Decisão**: Desenvolver o script utilizando requests em conjunto com `io.BytesIO` e `zipfile`.

**Justificativa**: Optei por realizar o download e a descompactação dos arquivos .zip inteiramente em memória (RAM), sem a necessidade de salvar arquivos temporários em disco, o que reduz drasticamente a latência de I/O e torna o processamento significativamente mais rápido. Além de manter o ambiente limpo ao evitar o acúmulo de arquivos residuais no sistema operacional, essa abordagem assegura a compatibilidade com a nuvem (Cloud-Readiness), facilitando a migração para arquiteturas serverless (como AWS Lambda), que possuem armazenamento temporário limitado e efêmero.

### 5. Logging Estruturado

**Decisão**: Implementação de logging com formato padronizado

**Justificativa**: O logging estruturado é fundamental para ETLs em produção, onde rastreabilidade e debugging são essenciais. O formato padronizado segue padrões da indústria, facilitando parsing automático por ferramentas como CloudWatch. A diferenciação entre níveis (INFO, WARNING, ERROR) permite alertas focados em problemas específicos. Os logs permitem reconstruir a sequência de eventos quando um ETL falha.

### 6. Testes Unitários

**Decisão**: Criação de Testes Unitários para a Etapa.

**Justificativa**: A inclusão de testes unitários no arquivo test_etl.py adiciona uma camada indispensável de segurança e confiabilidade ao pipeline de dados. Ao validar isoladamente a lógica de padronização e limpeza das colunas — uma etapa crítica e propensa a erros na fase de transformação —, garantimos que as regras de negócio estejam corretas antes de submeter o sistema a cargas reais. Essa prática preventiva é fundamental para evitar o desperdício de tempo e recursos computacionais, impedindo que falhas estruturais sejam descobertas apenas após o processamento oneroso de gigabytes de dados.

## ☁️ Versão Cloud (Diferencial)

**Decisão**: Criação do script `etl_aws_demo.py` simulando uma função AWS Lambda integrada ao S3. 

**Justificativa**: Mesmo fazendo o teste localmente, incluí um exemplo de como seria a versão na nuvem. A arquitetura usa serviços da AWS que não exigem gerenciamento de servidores, o que deixa o projeto mais barato e rápido, além de manter os arquivos salvos de forma independente do processamento.

### Componentes Utilizados

- **AWS Lambda**: Execução serverless do ETL
- **Amazon S3**: Armazenamento dos dados processados
- **EventBridge**: Agendamento de execuções (implícito na arquitetura)

### Vantagens da Abordagem Cloud

- A arquitetura proposta oferece alta escalabilidade através do processamento automático e sem a necessidade de gerenciamento de servidores (serverless), aliado a um modelo de custo eficiente onde se paga apenas pelos recursos efetivamente utilizados (pay-per-use). Além disso, a solução garante a confiabilidade inerente à infraestrutura gerenciada pela AWS e assegura total disponibilidade, permitindo o acesso seguro aos dados a partir de qualquer lugar.

### Adaptações Realizadas

- Substituição de `load()` por `load_to_s3()`
- Uso de `StringIO` para buffer em memória (evita escrita local)
- Implementação de `lambda_handler()` para integração com Lambda
- Retorno de status HTTP para monitoramento

## 🧪 Testes

### Estrutura de Testes

O arquivo `test_etl.py` implementa testes unitários utilizando `unittest`, framework padrão do Python.

### Teste Implementado

**`standart_columns_test()`**: Valida a normalização de colunas
- Verifica conversão para uppercase
- Verifica remoção de espaços em branco
- Garante que colunas antigas não existem após transformação

## 📦 Dependências

### Bibliotecas Utilizadas

```python
requests      # Requisições HTTP para API da ANS
pandas        # Manipulação e processamento de dados
zipfile       # Extração de arquivos ZIP
boto3         # Cliente AWS (apenas versão cloud)
logging       # Sistema de logs
unittest      # Framework de testes
```

### Instalação

```bash
pip install requests pandas boto3
```

## 🚀 Como Executar

### Versão Local

```bash
cd 1-integracao-API
```

```bash
python etl_ans.py
```

**Resultado**: Arquivo `consolidado_despesas.csv` gerado em `dados_brutos/`

### Versão Cloud (AWS Lambda)

1. Configurar credenciais AWS:
```bash
aws configure
```

2. Criar bucket S3:
```bash
aws s3 mb s3://joao-ans-raw-data
```

3. Executar localmente (simulação):
```bash
python etl_aws_demo.py
```

4. Para deploy em Lambda, empacotar e fazer upload da função

### Executar Testes

```bash
python test_etl.py
```

## 📊 Dados Processados

### Fonte
- **URL Base**: `https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/`
- **Formato**: Arquivos ZIP contendo CSVs
- **Período**: Trimestres de 2024 (1T, 2T, 3T)

### Saída
- **Arquivo**: `consolidado_despesas.csv`
- **Formato**: CSV delimitado por ponto e vírgula (`;`)
- **Encoding**: UTF-8
- **Coluna Adicional**: `TRIMESTRE_REF` (identificação do trimestre)

## 🔒 Boas Práticas Implementadas

### 1. **Tratamento de Erros**
- Try-except em pontos críticos
- Logging de erros detalhado
- Continuidade do processo mesmo com falhas parciais

### 2. **Separação de Responsabilidades**
- Métodos com responsabilidades únicas
- Código modular e reutilizável

### 3. **Versionamento**
- Uso adequado de Git (`.gitignore` configurado)
- Estrutura de pastas organizada

### 4. **Documentação**
- Código comentado onde necessário
- README completo e detalhado


## 🎓 Conhecimentos Demonstrados

### Fundamentos de Programação
- Orientação a Objetos
- Estruturas de dados (listas, dicionários)
- Manipulação de arquivos
- Tratamento de exceções

### Bibliotecas e Frameworks
- Pandas para manipulação de dados
- Requests para integração HTTP
- Boto3 para serviços AWS
- Unittest para testes

### Arquitetura e Design
- Padrão ETL bem estruturado
- Separação de responsabilidades
- Código extensível e manutenível


## 📝 Notas Finais

Este projeto demonstra:
- ✅ Conhecimentos fundamentais de programação Python
- ✅ Código claro, organizado e bem estruturado
- ✅ Boas práticas de desenvolvimento
- ✅ Documentação completa e justificativa de decisões técnicas
- ✅ Implementação de testes
- ✅ Preocupação com performance
- ✅ Arquitetura bem planejada
- ✅ Uso adequado de versionamento (Git)
- ✅ Aplicação de recursos de nuvem (AWS)

---



