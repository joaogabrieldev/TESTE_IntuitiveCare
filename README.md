<div align="center">

# 🏥 Teste Técnico - Intuitive Care

### Pipeline Completo de Dados: ETL, Transformação, Banco de Dados e Dashboard Web

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.43-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=FF9900)](https://aws.amazon.com/)

</div>

---

## 📋 Índice

- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [🏗️ Arquitetura Geral](#️-arquitetura-geral)
- [📦 Tecnologias e Bibliotecas](#-tecnologias-e-bibliotecas)
- [🎯 As 4 Etapas](#-as-4-etapas)
- [🔧 Padrões de Projeto](#-padrões-de-projeto)
- [🚀 Como Executar](#-como-executar)
- [📊 Estrutura de Dados](#-estrutura-de-dados)
- [👨‍💻 Desenvolvedor](#-desenvolvedor)

---

## 📖 Sobre o Projeto

Este projeto foi desenvolvido como teste técnico para a **Intuitive Care**, demonstrando habilidades completas em engenharia de dados e desenvolvimento full stack. A solução implementa um pipeline end-to-end que:

- 🔄 **Extrai** dados de demonstrações contábeis da ANS (Agência Nacional de Saúde Suplementar)
- 🔧 **Transforma** e valida os dados com regras de negócio
- 💾 **Carrega** em banco de dados relacional normalizado
- 📊 **Visualiza** através de dashboard web interativo

O projeto está organizado em **4 etapas sequenciais**, cada uma com objetivos específicos e documentação detalhada.

---

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    Fonte de Dados                            │
│         API ANS - Demonstrações Contábeis                     │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 1: Integração API                                     │
│  • Extração de dados trimestrais                             │
│  • Transformação e padronização                              │
│  • Consolidação em CSV                                       │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 2: Transformação de Dados                            │
│  • Validação de CNPJ                                        │
│  • Enriquecimento com cadastro ANS                          │
│  • Agregação estatística                                     │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 3: Banco de Dados                                     │
│  • Modelagem relacional normalizada                         │
│  • Carga de dados via ETL Python                            │
│  • Queries analíticas complexas                             │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 4: Web API & Dashboard                               │
│  • API RESTful (FastAPI)                                    │
│  • Frontend React/Next.js                                   │
│  • Visualizações interativas                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Tecnologias e Bibliotecas

### 🐍 Backend (Python)

<div align="center">

![Python](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg) ![FastAPI](https://cdn.simpleicons.org/fastapi/009688) ![SQLAlchemy](https://cdn.simpleicons.org/sqlalchemy/1F4E79) ![Pandas](https://cdn.simpleicons.org/pandas/150458) ![NumPy](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg)

</div>

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| **pandas** | 3.0.0 | Manipulação e processamento de dados tabulares |
| **numpy** | 2.4.1 | Cálculos numéricos otimizados e estatísticas |
| **requests** | 2.32.5 | Requisições HTTP para API da ANS |
| **boto3** | 1.42.39 | SDK AWS para integração com S3 e Lambda |
| **SQLAlchemy** | 2.0.46 | ORM para gerenciamento de banco de dados |
| **fastapi** | 0.128.1 | Framework web moderno e performático |
| **uvicorn** | 0.40.0 | Servidor ASGI para FastAPI |
| **pydantic** | 2.12.5 | Validação de dados e modelos |
| **openpyxl** | 3.1.5 | Leitura de arquivos Excel |

### ⚛️ Frontend (TypeScript/React)

<div align="center">

![Next.js](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg) ![React](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg) ![TypeScript](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg) ![Tailwind CSS](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg)

</div>

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| **next** | 16.1.6 | Framework React com App Router |
| **react** | 19.2.3 | Biblioteca de interface de usuário |
| **typescript** | 5.x | Tipagem estática para JavaScript |
| **axios** | 1.13.4 | Cliente HTTP para comunicação com API |
| **@tanstack/react-query** | 5.90.20 | Gerenciamento de estado e cache |
| **chart.js** | 4.5.1 | Biblioteca de gráficos |
| **react-chartjs-2** | 5.3.1 | Wrapper React para Chart.js |
| **tailwindcss** | 4.x | Framework CSS utility-first |
| **zod** | 4.3.6 | Validação de schemas TypeScript |

### 🗄️ Banco de Dados

<div align="center">

![SQLite](https://cdn.simpleicons.org/sqlite/003B57) ![MySQL](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg)

</div>

- **SQLite**: Banco de dados embutido para desenvolvimento e testes
- **MySQL**: Compatibilidade com queries analíticas (sintaxe adaptada)

### ☁️ Cloud (AWS)

<div align="center">

![AWS](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg) ![Lambda](https://cdn.simpleicons.org/awslambda/FF9900) ![S3](https://cdn.simpleicons.org/amazons3/569A31)

</div>

- **AWS Lambda**: Execução serverless dos scripts ETL
- **Amazon S3**: Armazenamento de dados processados
- **EventBridge**: Agendamento de execuções (arquitetura proposta)

---

## 🎯 As 4 Etapas

### 📥 Etapa 1: Integração de API - ETL de Dados ANS

<div align="center">

![Python](https://skillicons.dev/icons?i=python) ![AWS](https://skillicons.dev/icons?i=aws)

</div>

**Objetivo**: Extrair, transformar e carregar dados trimestrais de demonstrações contábeis da ANS.

**Principais Funcionalidades**:
- ✅ Extração automática de múltiplos trimestres via API pública
- ✅ Processamento em memória (sem arquivos temporários)
- ✅ Tratamento robusto de encoding (latin1 → utf-8)
- ✅ Normalização de colunas e padronização de dados
- ✅ Versão local e cloud (AWS Lambda + S3)

**Arquivos Principais**:
- `etl_ans.py` - Implementação local
- `etl_aws_demo.py` - Versão serverless para AWS
- `test_etl.py` - Testes unitários

**Padrão de Design**: Classe Orientada a Objetos com separação de responsabilidades (ETL)

---

### 🔄 Etapa 2: Transformação e Validação de Dados

<div align="center">

![Python](https://skillicons.dev/icons?i=python) ![Pandas](https://skillicons.dev/icons?i=pandas)

</div>

**Objetivo**: Qualificar, validar e enriquecer os dados brutos com regras de negócio.

**Principais Funcionalidades**:
- ✅ Validação algorítmica de CNPJ (dígitos verificadores)
- ✅ Enriquecimento com cadastro oficial de operadoras (ANS)
- ✅ Cálculo de métricas estatísticas (Soma, Média, Desvio Padrão)
- ✅ Filtragem de dados inválidos
- ✅ Agregação por UF e ordenação por despesas

**Arquivos Principais**:
- `transformacao_dados.py` - Pipeline de transformação local
- `transformacao_aws_demo.py` - Versão cloud
- `test_transformacao.py` - Testes de validação de CNPJ

**Padrão de Design**: ETL encapsulado em classes com métodos estáticos

---

### 💾 Etapa 3: Banco de Dados e Análise

<div align="center">

![SQL](https://skillicons.dev/icons?i=sqlite) ![Python](https://skillicons.dev/icons?i=python)

</div>

**Objetivo**: Modelar esquema relacional e executar queries analíticas complexas.

**Principais Funcionalidades**:
- ✅ Modelagem normalizada (tabelas separadas)
- ✅ Carga automatizada via Python (sanitização de dados)
- ✅ Queries analíticas complexas (CTEs, Joins, Agregações)
- ✅ Compatibilidade SQLite e MySQL
- ✅ Tratamento de encoding e tipagem de dados

**Arquivos Principais**:
- `ddl_db.sql` - Definição das tabelas
- `carga_banco.py` - Script ETL de carga
- `queries_analiticas.sql` - Consultas de negócio
- `queries_db.sql` - Queries de validação

**Padrão de Design**: ELT (Extract, Load, Transform) híbrido

**Queries Analíticas**:
1. **Crescimento de Despesas**: Top 5 operadoras com maior crescimento percentual
2. **Distribuição Geográfica**: Estados com maiores despesas e média por operadora
3. **Performance Consistente**: Operadoras acima da média em 2+ trimestres

---

### 🌐 Etapa 4: Desenvolvimento Full Stack - API e Dashboard

<div align="center">

![Next.js](https://skillicons.dev/icons?i=nextjs) ![React](https://skillicons.dev/icons?i=react) ![TypeScript](https://skillicons.dev/icons?i=typescript) ![FastAPI](https://skillicons.dev/icons?i=fastapi)

</div>

**Objetivo**: Desenvolver aplicação web completa para visualização e análise dos dados.

**Backend (FastAPI)**:
- ✅ API RESTful com documentação Swagger automática
- ✅ Endpoints para listagem, busca e detalhamento
- ✅ Middleware CORS configurado
- ✅ Queries otimizadas com paginação

**Frontend (Next.js + React)**:
- ✅ Dashboard interativo com busca em tempo real
- ✅ Paginação de milhares de registros
- ✅ Gráficos dinâmicos (Chart.js)
- ✅ Página de detalhes por operadora
- ✅ Gerenciamento de estado com React Query
- ✅ Tipagem completa com TypeScript

**Arquivos Principais**:
- `server/main.py` - API FastAPI
- `web/src/app/` - Páginas Next.js
- `web/src/hooks/` - Custom hooks para dados
- `web/src/types/` - Definições TypeScript

**Padrão de Design**: Arquitetura de componentes funcionais com hooks

---

## 🔧 Padrões de Projeto

### 🏛️ Arquitetura

- **ETL/ELT**: Pipeline de dados estruturado em etapas claras
- **Separação de Responsabilidades**: Cada etapa tem objetivo único e bem definido
- **Modularidade**: Código organizado em classes e funções reutilizáveis

### 🎨 Design Patterns

1. **Orientação a Objetos**: Classes encapsulando lógica ETL
2. **Factory Pattern**: Criação de instâncias de banco de dados
3. **Repository Pattern**: Abstração de acesso a dados (SQLAlchemy)
4. **Custom Hooks**: Lógica de dados reutilizável no frontend
5. **Provider Pattern**: Context API para React Query

### 📐 Princípios SOLID

- **Single Responsibility**: Cada classe/método tem uma responsabilidade única
- **Open/Closed**: Extensível sem modificar código existente
- **Dependency Inversion**: Uso de abstrações (SQLAlchemy, React Query)

### 🧪 Qualidade de Código

- ✅ **Testes Unitários**: Validação de lógica crítica (CNPJ, normalização)
- ✅ **Tratamento de Erros**: Try-except em pontos críticos
- ✅ **Logging Estruturado**: Rastreabilidade completa do pipeline
- ✅ **Type Safety**: TypeScript no frontend, type hints no Python
- ✅ **Documentação**: READMEs detalhados em cada etapa

### 🔒 Boas Práticas

- **Encoding Robusto**: Tratamento múltiplo de encoding (latin1, utf-8)
- **Validação de Dados**: Regras de negócio aplicadas (CNPJ, valores numéricos)
- **Normalização de Dados**: Padronização de colunas e formatos
- **Performance**: Processamento em memória, queries otimizadas
- **Cloud-Ready**: Versões adaptadas para AWS Lambda/S3

---

## 🚀 Como Executar

### 📋 Pré-requisitos

- Python 3.8+
- Node.js 18+
- pnpm (ou npm/yarn)

### 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/joaogabrieldev/teste_intuitivecare.git
cd teste_intuitivecare
```

2. **Configure o ambiente Python**:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Execute as etapas sequencialmente**:

#### Etapa 1: Integração API
```bash
cd 1-integracao-API
python etl_ans.py
```

#### Etapa 2: Transformação
```bash
cd ../2-transfomarcao-dados
python transformacao_dados.py
```

#### Etapa 3: Banco de Dados
```bash
cd ../3-banco-de-dados
python carga_banco.py
```

#### Etapa 4: Web API e Dashboard
```bash
# Backend
cd ../4-web-api/server
python carga_banco.py  # Carregar dados no banco
uvicorn main:app --reload

# Frontend (novo terminal)
cd ../4-web-api/web
pnpm install
pnpm dev
```

### 🌐 Acessos

- **API Backend**: http://127.0.0.1:8000
- **Swagger UI**: http://127.0.0.1:8000/docs
- **Dashboard**: http://localhost:3000

---

## 📊 Estrutura de Dados

### 🗂️ Modelo Relacional

```
operadoras_cadastral
├── REG_ANS (PK)
├── CNPJ
├── RAZAO_SOCIAL
├── MODALIDADE
├── UF
└── CIDADE

detalhe_despesas
├── ID (PK)
├── REG_ANS (FK)
├── DATA_EVENTO
├── EVENTO
├── DESCRICAO
└── VL_SALDO_FINAL
```

### 📈 Dados Processados

- **Fonte**: API ANS - Demonstrações Contábeis
- **Período**: Trimestres de 2024 (1T, 2T, 3T)
- **Formato**: CSV → SQLite → JSON (API)
- **Encoding**: UTF-8 (normalizado)

---

## 👨‍💻 Desenvolvedor

<div align="center">

### João Gabriel Rocha

[![GitHub](https://img.shields.io/badge/GitHub-joaogabrieldev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/joaogabrieldev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaogabrielrocha-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/joaogabrielrocha)

</div>

---

## 📝 Licença

Este projeto foi desenvolvido como teste técnico para a **Intuitive Care**.

---

<div align="center">

**Desenvolvido com ❤️ usando Python, React e TypeScript**

![Python](https://skillicons.dev/icons?i=python) ![React](https://skillicons.dev/icons?i=react) ![TypeScript](https://skillicons.dev/icons?i=typescript) ![AWS](https://skillicons.dev/icons?i=aws)

</div>

