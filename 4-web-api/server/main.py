from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List, Optional, Any
import os

app = FastAPI(
    title="Intuitive Care API",
    description="API de Operadoras e Despesas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "intuitive_care.db")

print(f"📂 PASTA DO ARQUIVO: {BASE_DIR}")
print(f"🗄️ CAMINHO DO BANCO: {DB_PATH}")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class Operadora(BaseModel):
    REG_ANS: str
    CNPJ: str
    RAZAO_SOCIAL: str
    UF: Optional[str] = None
    MODALIDADE: Optional[str] = None
    TOTAL_DESPESAS: Optional[float] = None

class Despesa(BaseModel):
    DESCRICAO: str
    DATA_EVENTO: Optional[str] = None
    VALOR: float

class PaginatedResponse(BaseModel):
    data: List[Any]
    total: int
    page: int
    limit: int
    total_pages: int

class Estatisticas(BaseModel):
    total_geral_despesas: float
    media_por_operadora: float
    top_5_operadoras: List[dict]

@app.get("/api/operadoras", response_model=PaginatedResponse)
@app.get("/api/operadoras", response_model=PaginatedResponse)
def listar_operadoras(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        query: Optional[str] = Query(None)
):
    try:
        offset = (page - 1) * limit

        with engine.connect() as conn:
            sql_base = "FROM operadoras_cadastral WHERE 1=1"

            # --- CORREÇÃO 1: Removi o ": dict[str, Any]" para evitar erro de versão do Python ---
            params = {"limit": limit, "offset": offset}

            if query:
                sql_base += " AND (RAZAO_SOCIAL LIKE :busca OR CNPJ LIKE :busca)"
                params["busca"] = f"%{query}%"

            # Conta o total
            query_total = text(f"SELECT COUNT(*) {sql_base}")
            total = conn.execute(query_total, params).scalar() or 0

            # Busca os dados
            query_dados = text(
                f"SELECT REG_ANS, CNPJ, RAZAO_SOCIAL, UF, MODALIDADE {sql_base} LIMIT :limit OFFSET :offset")

            # --- CORREÇÃO 2: Força conversão para dicionário (dict) ---
            result = [dict(row) for row in conn.execute(query_dados, params).mappings().all()]

        import math
        total_pages = math.ceil(total / limit) if total > 0 else 0

        return {
            "data": result,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    except Exception as e:
        # --- DEBUG: Isso vai mostrar o erro vermelho no seu terminal! ---
        print(f"❌ ERRO GRAVE NA ROTA OPERADORAS: {e}")
        # Relança o erro para o navegador ver o 500
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/operadoras/{cnpj}", response_model=Operadora)
def detalhes_operadora(cnpj: str):
    with engine.connect() as conn:
        query = text("SELECT * FROM operadoras_cadastral WHERE CNPJ = :cnpj")
        result = conn.execute(query, {"cnpj": cnpj}).mappings().first()

    if not result:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return result


@app.get("/api/operadoras/{cnpj}/despesas", response_model=List[Despesa])
def historico_despesas(cnpj: str):
    with engine.connect() as conn:
        query = text("""
            SELECT d.DESCRICAO, d.DATA_EVENTO, d.VL_SALDO_FINAL as VALOR
            FROM detalhe_despesas d
            JOIN operadoras_cadastral c ON d.REG_ANS = c.REG_ANS
            WHERE c.CNPJ = :cnpj
            ORDER BY d.DATA_EVENTO DESC LIMIT 100
        """)
        result = conn.execute(query, {"cnpj": cnpj}).mappings().all()
    return result


@app.get("/api/estatisticas", response_model=Estatisticas)
def obter_estatisticas():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT SUM(TOTAL_DESPESAS) FROM despesas_agregadas")).scalar() or 0.0
        media = conn.execute(text("SELECT AVG(TOTAL_DESPESAS) FROM despesas_agregadas")).scalar() or 0.0
        top_5 = conn.execute(text(
            "SELECT RAZAO_SOCIAL, UF, TOTAL_DESPESAS FROM despesas_agregadas ORDER BY TOTAL_DESPESAS DESC LIMIT 5")).mappings().all()

    return {
        "total_geral_despesas": total,
        "media_por_operadora": media,
        "top_5_operadoras": top_5
    }
