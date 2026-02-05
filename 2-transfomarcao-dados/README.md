# Etapa 2: Transformação e Validação de Dados

## 🎯 Objetivo da Etapa

Esta etapa foca na qualificação e enriquecimento dos dados brutos obtidos anteriormente. Os objetivos principais são:
- Implementar regras de validação de negócio (CNPJ, valores numéricos).
- Enriquecer os dados financeiros cruzando-os com o cadastro oficial de operadoras da ANS.
- Calcular métricas estatísticas agregadas (Soma, Média, Desvio Padrão) para análise.

## 🏗️ Arquitetura

### Estrutura do Projeto

```
2-transformacao-dados/ 
    ├── dados_brutos/ # Local dos CSVs de entrada e saída 
    ├── transformacao_dados.py # Script principal (ETL Local) 
    ├── transformacao_aws_demo.py # Script adaptado para Cloud (AWS Lambda/S3) 
    ├── test_transformacao.py # Testes unitários de validação 
    ├── .gitignore # Arquivos ignorados 
    └── README.md # Documentação da etapa
```

### Design Pattern

O código segue o padrão **ETL (Extract, Transform, Load)** encapsulado em classes:
- **`DataTransformer`**: Classe responsável por orquestrar todo o pipeline local.
- **`validate_cnpj()`**: Método estático puro para validação algorítmica.
- **`process()`**: Método principal que executa a sequência lógica de transformação.

## 🔧 Decisões Técnicas e Trade-offs

### 1. Validação de Dados (CNPJ)

**Decisão**: Validação algorítmica estrita (Dígitos Verificadores).

**Justificativa**: Em vez de apenas verificar o formato (Regex) ou comprimento, implementei o cálculo oficial dos dígitos verificadores (Módulo 11).
- **Trade-off**: Processamento levemente mais custoso vs. Alta confiabilidade.
- **Estratégia para Inválidos**: Registros com CNPJs matematicamente inválidos são **descartados** (`df_merged[df_merged["CNPJ_VALIDO"] == True]`).
    - *Pró*: Garante que o relatório final contenha apenas empresas fiscalmente consistentes.
    - *Contra*: Perda de dados se houver erros de digitação na fonte original. Considerei que, para análises financeiras oficiais, a integridade do identificador fiscal é inegociável.

### 2. Enriquecimento de Dados (Join)

**Decisão**: Join do tipo `INNER JOIN` entre dados contábeis e cadastrais.

**Justificativa**: O objetivo é analisar despesas de operadoras *ativas* e com cadastro regular.
- **Trade-off**:
    - `INNER JOIN`: Mantém apenas operadoras presentes em ambas as bases.
    - *Motivo da escolha*: Operadoras que estão no consolidado contábil mas não no cadastro de ativas (possivelmente canceladas ou liquidadas) não devem compor a análise de mercado atual. Da mesma forma, operadoras cadastradas sem despesas reportadas são irrelevantes para esta análise específica de custos.

### 3. Agregação e Estatística

**Decisão**: Cálculo de métricas descritivas (Soma, Média, Desvio Padrão) por UF.

**Justificativa**:
- **Desvio Padrão**: Incluído para identificar volatilidade nos gastos. Operadoras com desvio padrão alto indicam fluxo de caixa instável ou eventos de despesas atípicos no período.
- **Ordenação**: Ordenado por `TOTAL_DESPESAS` (decrescente) para priorizar a visualização dos maiores players do mercado ("Pareto").

### 4. Tratamento de Arquivos e Encoding

**Decisão**: Leitura flexível (`utf-8-sig` e `latin1`) e padronização de colunas (`strip().upper()`).

**Justificativa**: Arquivos governamentais frequentemente misturam encodings. O script tenta ler o cadastro oficial em `latin1` (padrão comum em legados) e os dados processados em `utf-8`. A normalização dos nomes das colunas previne erros de `KeyError` causados por espaços invisíveis ou variações de caixa (ex: "Razao Social" vs "RAZAO SOCIAL").

## ☁️ Versão Cloud (Diferencial)

O arquivo `transformacao_aws_demo.py` adapta a lógica para execução Serverless:
- **Leitura/Escrita**: Substitui o sistema de arquivos local (`open()`) por chamadas via `boto3` direto ao S3.
- **Buffer em Memória**: Utiliza `io.BytesIO` e `io.StringIO` para manipular CSVs e ZIPs sem disco físico, requisito para performance em AWS Lambda.
- **Segurança**: As credenciais não estão hardcoded, sendo gerenciadas via IAM Roles do ambiente.

## 🧪 Testes Unitários

O arquivo `test_transformacao.py` foca na lógica mais crítica do negócio: **Validação de CNPJ**.
- Casos de Teste:
    - ✅ CNPJ Válido com máscara.
    - ✅ CNPJ Válido apenas números.
    - ❌ CNPJ com dígito verificador errado.
    - ❌ CNPJ com tamanho incorreto.
    - ❌ CNPJ com todos os dígitos iguais (ex: 11.111.111/1111-11), que passa no cálculo matemático mas é inválido por regra de negócio.

## 📦 Dependências

```python
pandas      # Manipulação de dados tabulares
numpy       # Cálculos numéricos otimizados
requests    # Download do cadastro atualizado
boto3       # SDK AWS (apenas versão cloud)
```

### 🚀 Como Executar
#### Versão Local
1. Certifique-se de que o arquivo consolidado_despesas.csv da Etapa 1 esteja na pasta dados_brutos/.

2. Execute o script:

```Bash
python transformacao_dados.py
```
**Saída**:

- Arquivo dados_brutos/despesas_agregadas.csv

- Arquivo compactado Teste_Joao-Gabriel.zip contendo o resultado final.

**Executar Testes**
```Bash
python test_transformacao.py
```