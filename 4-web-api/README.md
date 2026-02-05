# Etapa 4: Desenvolvimento Full Stack - API e Dashboard

## 🎯 Objetivo da Etapa

Desenvolver uma aplicação web completa para visualização e análise dos dados processados, composta por:

- **Backend**: API RESTful para servir os dados das operadoras e despesas.
- **Frontend**: Dashboard interativo para listagem, busca e visualização gráfica.
- **Banco de Dados**: Persistência estruturada dos dados transformados.

## 🏗️ Arquitetura

### Estrutura do Projeto

O projeto foi dividido em dois monorepositórios (Backend e Frontend) para manter a separação de responsabilidades.

```
    4-web-api/

        ├── server/ # Backend (Python/FastAPI)
            │
            ├── csv_files/ # Dados brutos para carga
            │
            ├── carga_banco.py # Script ETL para povoar o banco
            │
            ├── main.py # Aplicação Principal da API
            │
            ├── intuitive_care.db # Banco de Dados SQLite
            │
            └── requirements.txt # Dependências Python

        ├── frontend/ # Frontend (Node/Next.js)
            │
            ├── src/
            │
            │
            ├── app/ # Páginas (Dashboard e Detalhes)
            │
            │
            ├── components/ # Componentes visuais
            │
            │
            ├── hooks/ # Custom Hooks (Lógica de dados)
            │
            │
            └── types/ # Tipagem TypeScript
            │
            └── package.json # Dependências Node

```

## 🔧 Decisões Técnicas

### 1. Backend: FastAPI e SQLite

**Decisão**: Utilização do FastAPI com banco de dados SQLite.

**Justificativa**: O FastAPI foi escolhido por sua alta performance e geração automática de documentação (Swagger UI), essencial para testes rápidos. O SQLite foi adotado pela portabilidade (arquivo único) e simplicidade de configuração. Para contornar limitações de concorrência do SQLite em ambiente web, utilizei a flag `check_same_thread=False` na engine do SQLAlchemy, permitindo múltiplas requisições simultâneas sem bloqueio.

### 2. Frontend com React ao invés do Vue.js

**Decisão**: Adoção do ecossistema React (Next.js + TypeScript) em vez de Vue.js.

**Justificativa**: A escolha pelo ecossistema **React (Next.js + TypeScript)** priorizou a proficiência técnica e a robustez arquitetural. Ao utilizar minha stack principal, garanti uma entrega veloz e eliminei a curva de aprendizado, alavancando uma arquitetura baseada em componentes funcionais e hooks que, aliada à tipagem estrita do TypeScript, estabelece um contrato de dados rígido e seguro entre Backend e Frontend. Além disso, a estrutura do Next.js (App Router) impõe padrões de organização que favorecem a separação de responsabilidades (Client vs. Server Components), resultando em um código mais limpo, modular e escalável — prevenindo erros críticos em tempo de compilação de forma mais eficaz do que uma implementação padrão em Vue. 

### 3. Gerenciamento de Estado e Cache

**Decisão**: Implementação do **TanStack Query (React Query)**.

**Justificativa**: Para evitar requisições desnecessárias e melhorar a UX, o **TanStack Query** gerencia o estado do servidor no frontend. Ele oferece cache automático, refetching em segundo plano e estados de carregamento (`isLoading`), garantindo que o dashboard seja extremamente reativo e veloz, sem sobrecarregar a API.

### 4. Cliente HTTP e Resiliência

**Decisão**: Instância customizada do Axios dentro de Hooks.

**Justificativa**: Para evitar problemas de importação cíclica e garantir a tipagem correta dos dados retornados, optei por instanciar o cliente `axios` diretamente nos Hooks de serviço. Isso isola a lógica de conexão e facilita a manutenção das URLs base (localhost), além de permitir interceptação de erros de forma centralizada.

### 5. Visualização de Dados

**Decisão**: Integração com **Chart.js** e **React-Chartjs-2**.

**Justificativa**: O Chart.js é uma biblioteca leve e flexível para renderização de gráficos. Foi utilizada para criar a visualização das "Top 5 Maiores Despesas", oferecendo feedback visual imediato sobre os dados financeiros mais críticos, complementando a visão tabular.

## 🚀 Funcionalidades Implementadas

### Backend (API)

- **GET /api/operadoras**: Listagem paginada com filtro de busca (LIKE) por Razão Social ou CNPJ.
- **GET /api/operadoras/{cnpj}**: Detalhes cadastrais de uma operadora específica.
- **GET /api/operadoras/{cnpj}/despesas**: Histórico financeiro detalhado.
- **GET /api/estatisticas**: Agregação de dados para alimentar os gráficos.
- **Middleware CORS**: Configurado para aceitar requisições do Frontend local.

### Frontend (Dashboard)

- **Busca em Tempo Real**: Filtro de operadoras por texto.
- **Paginação**: Navegação fluida entre milhares de registros.
- **Gráficos Dinâmicos**: Visualização estatística das maiores despesas.
- **Página de Detalhes**: View exclusiva com dados cadastrais e tabela de histórico financeiro.

## 📦 Dependências

### Backend (Python)

```python
fastapi       # Framework Web
swagger       # Documentação de API (integrado automaticamente com FastAPI)
uvicorn       # Servidor ASGI
sqlalchemy    # ORM de Banco de Dados
pydantic      # Validação de Dados
pandas        # Leitura de CSVs para carga
```

### Frontend (Node.js)

```python
next          # Framework React
react         # Biblioteca de UI
axios         # Cliente HTTP
chart.js      # Gráficos
tailwindcss   # Estilização
@tanstack/react-query # Gerenciamento de Estado/Cache
```

## Como Executar

### 1. Preparação do Banco de Dados

Antes de iniciar, é necessário povoar o banco com os dados da Etapa 1.

```Bash
cd server
python carga_banco.py
```

_Aguarde a mensagem "Carga completa!"._

### 2. Iniciando o Backend

No terminal da pasta server:

```Bash
uvicorn main:app --reload

A API estará disponível em: http://127.0.0.1:8000

Documentação Swagger: http://127.0.0.1:8000/docs
```

### 3. Iniciando o Frontend

Em um novo terminal, na pasta frontend:

```Bash
npm install
npm run dev
```

```
Acesse o Dashboard em: 
http://localhost:3000
```

## Notas Finais

Esta etapa consolidou o projeto transformando dados brutos em informação visual acessível. A solução priorizou a experiência do usuário (UX) através de feedbacks visuais de carregamento e paginação, e a qualidade de código (DX) através de tipagem estrita e separação de conceitos.
