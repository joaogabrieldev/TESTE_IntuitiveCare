# Etapa 1: Integração de API - ETL de Dados ANS

## 📋 Visão Geral

Esta etapa implementa um processo ETL (Extract, Transform, Load) para coletar, processar e armazenar dados de demonstrações contábeis da Agência Nacional de Saúde Suplementar (ANS). O projeto foi desenvolvido seguindo boas práticas de engenharia de software, com foco em código limpo, manutenibilidade e escalabilidade.

## 🎯 Objetivo

Desenvolver uma solução robusta para:
- Extrair dados trimestrais de demonstrações contábeis da ANS via API pública
- Transformar e padronizar os dados coletados
- Carregar os dados consolidados em formato CSV (local) ou S3 (cloud)

## 🏗️ Arquitetura

### Estrutura do Projeto

```
1-integração-API/
├── etl_ans.py          # Implementação ETL local (sem cloud)
├── etl_aws_demo.py     # Implementação ETL com AWS (serverless)
├── test_etl.py         # Testes unitários
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Documentação do projeto
```

### Padrão de Design

O projeto utiliza o padrão **Classe Orientada a Objetos** com separação clara de responsabilidades:

- **`ETLEventsANS`**: Classe principal que encapsula toda a lógica ETL
- **`extract_and_transform()`**: Responsável pela extração e transformação dos dados
- **`load()` / `load_to_s3()`**: Responsável pelo carregamento dos dados processados
- **`implement()`**: Orquestra todo o processo ETL

## 🔧 Decisões Técnicas

### 1. Estruturação do Código

**Decisão**: Utilização de classe única com métodos bem definidos

**Justificativa**: A arquitetura orientada a objetos com classe única centraliza a lógica ETL, facilitando manutenção e correção de bugs. A estruturação em métodos bem definidos cria separação clara de responsabilidades (princípio SOLID). A mesma classe é reutilizada nas versões local e cloud (princípio DRY), garantindo consistência. A estrutura também facilita testes unitários isolados e melhora a legibilidade através de métodos auto-documentados.

### 2. Tratamento de Encoding

**Decisão**: Tentativa múltipla de encoding (latin1 → utf-8)

**Justificativa**: Dados governamentais brasileiros frequentemente apresentam inconsistências de encoding. Arquivos históricos da ANS podem usar diferentes encodings, exigindo abordagem robusta. A estratégia previne falhas silenciosas que corromperiam caracteres (ex: "ç" se tornando "Ã§"). Inicia-se com `latin1` (comum em sistemas legados) e faz fallback para `utf-8` (padrão moderno), utilizando `try-except` com `f.seek(0)` para resetar o ponteiro. Isso garante que o ETL lide com ambos os padrões sem overhead, mantendo integridade dos dados.

```python
try:
    df = pd.read_csv(f, sep=";", encoding="latin1", dtype=str)
except Exception:
    f.seek(0)
    df = pd.read_csv(f, sep=";", encoding="utf-8", dtype=str)
```

### 3. Normalização de Colunas

**Decisão**: Padronização de nomes de colunas (strip + uppercase)

**Justificativa**: Arquivos da ANS de diferentes trimestres podem apresentar variações críticas nos nomes de colunas (capitalização, espaçamento), causando erros em merge e análise. A normalização automática garante padrão rigoroso, eliminando variações de case e espaçamento. Isso é crítico ao consolidar múltiplos trimestres, garantindo que colunas com mesmo significado tenham exatamente o mesmo nome, tornando análises temporais viáveis. Facilita trabalho de desenvolvedores e analistas, pois consultas não precisam considerar variações, simplificando código e melhorando manutenibilidade.

### 4. Remoção de Duplicatas

**Decisão**: Uso de `drop_duplicates()` antes do carregamento

**Justificativa**: A deduplicação previne distorções em análises estatísticas e agregações. A duplicação pode surgir de execuções repetidas, sobreposições entre trimestres ou erros na fonte. Realizar no final do pipeline é superior porque o pandas otimiza internamente e ocorre em um único ponto, facilitando manutenção. Previne que análises sejam distorcidas (ex: registro contado múltiplas vezes inflaciona métricas), garantindo integridade essencial. Além disso, reduz espaço de armazenamento e custos, enquanto melhora performance de consultas downstream (join, groupby, indexação).

### 5. Logging Estruturado

**Decisão**: Implementação de logging com formato padronizado

**Justificativa**: O logging estruturado é fundamental para ETLs em produção, onde rastreabilidade e debugging são essenciais. O formato padronizado segue padrões da indústria, facilitando parsing automático por ferramentas como CloudWatch, ELK Stack ou Datadog. A diferenciação entre níveis (INFO, WARNING, ERROR) permite alertas focados em problemas críticos. Os logs permitem reconstruir a sequência de eventos quando um ETL falha. Em ambientes cloud como AWS Lambda, logs são automaticamente capturados pelo CloudWatch, permitindo dashboards, métricas e alertas.

### 6. Medição de Performance

**Decisão**: Inclusão de métricas de tempo de execução

**Justificativa**: A medição de tempo de execução é essencial em ETLs com grandes volumes, onde eficiência impacta custos. O estabelecimento de baseline permite comparações objetivas, identificando se mudanças melhoraram ou degradaram a performance. Fornece ponto de partida para análises mais profundas e identificação de gargalos. Em ambientes cloud como AWS Lambda, o tempo está diretamente relacionado a custos (cobrança por tempo e memória). Execuções muito longas podem exceder timeout ou gerar custos altos, tornando a medição essencial para dimensionar recursos. O monitoramento permite detectar degradação gradual e definir SLAs com alertas.

## ☁️ Versão Cloud (Diferencial)

A versão `etl_aws_demo.py` demonstra como o mesmo código pode ser adaptado para uma arquitetura serverless na AWS:

### Componentes Utilizados

- **AWS Lambda**: Execução serverless do ETL
- **Amazon S3**: Armazenamento dos dados processados
- **EventBridge**: Agendamento de execuções (implícito na arquitetura)

### Vantagens da Abordagem Cloud

1. **Escalabilidade**: Processamento automático sem gerenciamento de servidores
2. **Custo**: Pagamento apenas pelo uso (pay-per-use)
3. **Confiabilidade**: Infraestrutura gerenciada pela AWS
4. **Disponibilidade**: Acesso aos dados de qualquer lugar

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

### Boas Práticas Aplicadas

- Testes isolados e independentes
- Uso de dados mockados (StringIO)
- Assertions claras e específicas

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

### 3. **Configuração Centralizada**
- Parâmetros definidos no `__init__`
- Fácil manutenção e alteração

### 4. **Versionamento**
- Uso adequado de Git (`.gitignore` configurado)
- Estrutura de pastas organizada

### 5. **Documentação**
- Código comentado onde necessário
- README completo e detalhado

## 📈 Performance

O código foi otimizado para:
- **Streaming de dados**: Uso de `stream=True` em requisições HTTP
- **Processamento em memória**: Buffer de dados antes da consolidação
- **Remoção de duplicatas**: Otimização do dataset final

## 🔄 Fluxo de Execução

```
1. Inicialização
   └─> Preparação do ambiente (criação de diretórios)

2. Extração (Extract)
   └─> Para cada trimestre:
       ├─> Download do arquivo ZIP
       ├─> Extração dos CSVs
       └─> Leitura e bufferização dos dados

3. Transformação (Transform)
   └─> Normalização de colunas
   └─> Adição de coluna TRIMESTRE_REF
   └─> Consolidação de todos os DataFrames

4. Carregamento (Load)
   └─> Remoção de duplicatas
   └─> Exportação para CSV (local) ou S3 (cloud)
   └─> Logging de estatísticas
```

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

## 🚧 Melhorias Futuras

1. **Testes Adicionais**
   - Testes de integração
   - Testes de performance
   - Testes de tratamento de erros

2. **Otimizações**
   - Processamento paralelo de trimestres
   - Validação de schema dos dados
   - Compressão de arquivos de saída

3. **Monitoramento**
   - Integração com CloudWatch (AWS)
   - Alertas de falhas
   - Dashboards de métricas

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

**Desenvolvido com foco em qualidade, manutenibilidade e escalabilidade.**

