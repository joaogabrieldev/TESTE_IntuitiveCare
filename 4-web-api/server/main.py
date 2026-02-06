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
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "intuitive_care.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# --- MODELOS ---
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


# --- ROTAS ---

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
            params = {"limit": limit, "offset": offset}

            if query:
                sql_base += " AND (RAZAO_SOCIAL LIKE :busca OR CNPJ LIKE :busca)"
                params["busca"] = f"%{query}%"

            query_total = text(f"SELECT COUNT(*) {sql_base}")
            total = conn.execute(query_total, params).scalar() or 0

            query_dados = text(
                f"SELECT REG_ANS, CNPJ, RAZAO_SOCIAL, UF, MODALIDADE {sql_base} LIMIT :limit OFFSET :offset")
            result = [dict(row) for row in conn.execute(query_dados, params).mappings().all()]

        import math
        total_pages = math.ceil(total / limit) if total > 0 else 0

        return {"data": result, "total": total, "page": page, "limit": limit, "total_pages": total_pages}
    except Exception as e:
        print(f"ERRO LISTA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/operadoras/{cnpj}", response_model=Operadora)
def detalhes_operadora(cnpj: str):
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM operadoras_cadastral WHERE CNPJ = :cnpj")
            row = conn.execute(query, {"cnpj": cnpj}).mappings().first()
            if not row:
                raise HTTPException(status_code=404, detail="Operadora não encontrada")
            return dict(row)
    except Exception as e:
        print(f"ERRO DETALHES: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/operadoras/{cnpj}/despesas", response_model=List[Despesa])
def historico_despesas(cnpj: str):
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT d.DESCRICAO, d.DATA_EVENTO, d.VL_SALDO_FINAL as VALOR
                FROM detalhe_despesas d
                JOIN operadoras_cadastral c ON d.REG_ANS = c.REG_ANS
                WHERE c.CNPJ = :cnpj
                ORDER BY d.DATA_EVENTO DESC LIMIT 100
            """)
            return [dict(row) for row in conn.execute(query, {"cnpj": cnpj}).mappings().all()]
    except Exception as e:
        print(f"ERRO DESPESAS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/estatisticas", response_model=Estatisticas)
def obter_estatisticas():
    try:
        with engine.connect() as conn:
            total = conn.execute(text("SELECT SUM(TOTAL_DESPESAS) FROM despesas_agregadas")).scalar() or 0.0
            media = conn.execute(text("SELECT AVG(TOTAL_DESPESAS) FROM despesas_agregadas")).scalar() or 0.0

            top_5_query = text(
                "SELECT RAZAO_SOCIAL, UF, TOTAL_DESPESAS FROM despesas_agregadas ORDER BY TOTAL_DESPESAS DESC LIMIT 5")
            top_5 = [dict(row) for row in conn.execute(top_5_query).mappings().all()]

        return {
            "total_geral_despesas": total,
            "media_por_operadora": media,
            "top_5_operadoras": top_5
        }
    except Exception as e:
        print(f"ERRO ESTATISTICAS: {e}")
        raise HTTPException(status_code=500, detail=str(e))