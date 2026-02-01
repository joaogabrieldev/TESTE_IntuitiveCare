import pandas as pd
import requests
import os
import io
import numpy as np
import logging
import zipfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataTransformer:
    def __init__(self):
        self.input_file = os.path.join("dados_brutos", "consolidado_despesas.csv")
        self.output_file = "despesas_agregadas.csv"
        self.zip_filename = " Teste_João-Gabriel.zip"
        self.cadastral_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_Cadop.csv"

    def validate_cnpj(self, cnpj):
        cnpj_filtered = "".join(digito for digito in str(cnpj) if digito.isdigit())

        if len(cnpj_filtered) != 14 or cnpj_filtered == cnpj_filtered[0] * 14:
            return False

        def calcular_digito(parte_cnpj, pesos):
            soma_produtos = sum(int(digito) * peso for digito, peso in zip(parte_cnpj))

            resto = soma_produtos % 11
            return 0 if resto < 2 else 11 - resto

        pesos_primeiro_digito = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos_segundo_digito = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        primeiro_digito = calcular_digito(cnpj_filtered[:12], pesos_primeiro_digito)

        segundo_digito = calcular_digito(cnpj_filtered[:13], pesos_segundo_digito)

        return cnpj_filtered[-2:] == f"{primeiro_digito}{segundo_digito}"

    def load_data(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError("Arquivo {self.input_file} não encontrado.")

        logging.info("Carregando dados...")
        df = pd.read_csv(self.input_file, sep=";", encoding="utf-8", dtype=str)
        df.columns = [column.strip().upper() for column in df.columns]

        col_desc = [c for c in df.columns if "DESCRICAO" in c or "CONTA" in c][-1]

        df = df[df[col_desc].str.contains("EVENTO|SINISTRO|DESPESA", case=False, na=False)]

        logging.info(f"Dados filtrados carregados: {len(df)} linhas.")
        return df

    def get_cadastral_data(self):
        logging.info("Baixando Cadastro de Operadoras...")
        try:
            response = requests.get(self.cadastral_url, verify=False)
            df_cadastral = pd.read_csv(io.BytesIO(response.content), sep=";", encoding="latin1", dtype=str)
            df_cadastral.columns = [column.strip().upper() for column in df_cadastral.columns]
            return df_cadastral
        except Exception as error:
            logging.error(f"ERRO: {error}")
            return None

    def process(self):
        df_accounting = self.load_data()
        df_cadastral = self.get_cadastral_data()

        col_register_accounting = [column for column in df_accounting.columns if "REG" in column and "ANS" in column][0]

        col_register_cadastral = [column for column in df_cadastral.columns if "REGISTRO" in column and "ANS" in column][0]

        logging.info("Cruzando dados contábeis")
        df_merged = pd.merge(
            df_accounting,
            df_cadastral[[col]]
        )









