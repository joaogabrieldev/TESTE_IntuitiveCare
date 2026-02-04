import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DatabaseLoader:
    def __init__(self):
        self.db_name = "intuitive_care.db"
        self.connection_string = f"sqlite:///{self.db_name}"
        self.engine = create_engine(self.connection_string)

        DATA_DIR = "csv_files"

        self.files_config = [
            {
                "file": os.path.join(DATA_DIR, "consolidado_despesas.csv"),
                "table": "detalhe_despesas",
                "sep": ";",
                "encoding": "utf-8",
                "decimal": ","
            },
            {
                "file": os.path.join(DATA_DIR, "despesas_agregadas.csv"),
                "table": "despesas_agregadas",
                "sep": ";",
                "encoding": "utf-8-sig",
                "decimal": ","
            },
            {
                "file": os.path.join(DATA_DIR, "Relatorio_cadop.csv"),
                "table": "operadoras_cadastral",
                "sep": ";",
                "encoding": "latin1",
                "decimal": "."
            }
        ]

    def _load_single_file(self, config):
        filename = config["file"]
        tablename = config["table"]

        if not os.path.exists(filename):
            logging.warning(f"Arquivo '{filename}' não encontrado.")
            return

        logging.info(f"Lendo arquivo: {filename}...")

        try:
            df = pd.read_csv(
                filename,
                sep=config["sep"],
                encoding=config["encoding"],
                decimal=config["decimal"],
                dtype=str
            )

            # 1. Padroniza colunas (Maiúsculo e sem espaço)
            df.columns = [column.strip().upper().replace(" ", "_") for column in df.columns]

            # 2. RENOMEAÇÃO FORÇADA (Para corrigir o erro "no such column")
            # Isso garante que o banco tenha os nomes que a query espera
            rename_map = {
                "DATA": "DATA_EVENTO",
                "DT_UTILIZACAO": "DATA_EVENTO",
                "VL_COMERCIAL": "VALOR_COMERCIAL",
                "VALOR": "VALOR_COMERCIAL",
                "REGISTRO_ANS": "REG_ANS",
                "CD_OPERADORA": "REG_ANS",
                "REGISTRO_OPERADORA": "REG_ANS"  # Para a tabela de cadastro
            }
            df.rename(columns=rename_map, inplace=True)

            # --- DEBUG: Mostra no terminal quais colunas ficaram ---
            logging.info(f"Colunas finais na tabela '{tablename}': {df.columns.tolist()}")

            # 3. Conversão de números
            if "despesas" in tablename:
                cols_valor = [c for c in df.columns if "VALOR" in c or "TOTAL" in c or "MEDIA" in c or "DESVIO" in c]
                for column in cols_valor:
                    try:
                        df[column] = df[column].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
                        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0.0)
                    except Exception:
                        pass  # Ignora erros de conversão pontuais

            logging.info(f"Salvando tabela '{tablename}' no Banco...")
            df.to_sql(tablename, self.engine, if_exists="replace", index=False)
            logging.info(f"Sucesso! Tabela '{tablename}' criada.")

        except Exception as error:
            logging.error(f"ERRO ao processar {filename}: {error}")

    def load_all_files(self):
        logging.info("Iniciando carga...")
        for config in self.files_config:
            self._load_single_file(config)
        logging.info("Carga completa!")

    def execute_queries(self, sql_file):
        if not os.path.exists(sql_file):
            logging.warning(f"Arquivo '{sql_file}' não encontrado.")
            return

        logging.info(f"Executando queries do arquivo: {sql_file}")

        if sys.stdout.encoding != 'utf-8':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass

        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                queries = f.read().split(';')

            with self.engine.connect() as conn:
                for query in queries:
                    if query.strip():
                        print("-" * 60)
                        titulo = query.strip().splitlines()[0][:50]
                        print(f"Executando: {titulo}...")
                        try:
                            df_result = pd.read_sql_query(text(query), conn)

                            if not df_result.empty:
                                print("\nRESULTADO:")
                                print(df_result.head(5).to_string(index=False))
                            else:
                                print("\n(Query rodou mas não retornou dados)")

                        except Exception as error:
                            logging.error(f"Erro SQL: {error}")
                        print("-" * 60)
        except Exception as error:
            logging.error(f"Erro leitura arquivo: {error}")


if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.load_all_files()

    loader.execute_queries("queries_db.sql")