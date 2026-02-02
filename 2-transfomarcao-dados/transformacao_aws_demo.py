import pandas as pd
import requests
import io
import logging
import zipfile
import boto3
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class DataTransformerCloud:
    def __init__(self):
        self.bucket_name = os.environ.get("S3_BUCKET_NAME", "joao-ans-raw-data")
        self.input_key = "raw/consolidando_despesas.csv"
        self.output_key = "refined/Teste_Joao-Gabriel.zip"
        self.cadastral_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_Cadop.csv"
        self.s3_client = boto3.client("s3")

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

    def load_data_from_s3(self):
        logging.info(self.input_key)
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.input_key)

            csv_content = response["Body"].read()

            df = pd.read_csv(io.BytesIO(csv_content), sep=";", encoding="utf-8", dtype=str)
            df.columns = [column.strip().upper() for column in df.columns]

            col_desc = [column for column in df.columns if "DESCRICAO" in  column or "CONTA" in column][-1]
            df = df[df[col_desc].str.contains("EVENTO|SINISTRO|DESPESA", case=False, na=False)]
            logger.info(f"Dados do S3 carregados: {len(df)} linhas.")

            return df
        except Exception as error:
            logger.error(f"[ERRO]: {error}")
            raise error

    def get_cadastral_data(self):
        logger.info("Baixando Cadastros...")
        try:
            response = requests.get(self.cadastral_url, verify=False)
            df_cadastral = pd.read_csv(io.BytesIO(response.content), sep=";", encoding="utf-8")
            df_cadastral.columns = [column.strip().upper() for column in df_cadastral.columns]
            return df_cadastral

        except Exception as error:
            logger.error(f"ERRO no download do cadastro: {error}")
            return None




