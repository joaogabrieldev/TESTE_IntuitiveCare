import os
import requests
import zipfile
import pandas as pd
import io
import time
import logging
from io import StringIO
import boto3

# ARQUIVO PARA MOSTRAR COMO SERIA O CÓDIGO CASO FOSSE CLOUD SERVERLESS, COM AWS Lambda + Amazon S3 + EventBridge

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ETLEventsANS:
    def __init__(self):
        self.base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
        self.output_dir = "dados_brutos"
        self.final_filename = "consolidado_despesas.csv"
        self.trimesters = ["2024/01", "2024/02", "2024/03"]
        self.prepare_environment()

    def prepare_environment(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def extract_and_transform(self):
        data_buffer = []
        for trimester in self.trimesters:
            logging.info(f"Trimestre: {trimester}")
            try:
                year, tri = trimester.split("/")

                file_name = f"{int(tri)}T{year}.zip"
                full_url = f"{self.base_url}{year}/{file_name}"

                response = requests.get(full_url, stream=True)
                if response.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                        csv_files = [f for f in z.namelist() if f.lower().endswith(".csv")]

                        for file in csv_files:
                                with z.open(file) as f:
                                    try:
                                        df = pd.read_csv(f, sep=";", encoding="latin1", dtype=str)
                                    except Exception:
                                        f.seek(0)
                                        df = pd.read_csv(f, sep=";", encoding="utf-8", dtype=str)

                                    df.columns = [c.strip().upper() for c in df.columns]
                                    df["TRIMESTRE_REF"] = f"{tri}T{year}"
                                    data_buffer.append(df)
                else:
                    logging.warning(f"URL não encontrada: {full_url}")


            except Exception as error:
                logging.error(f"[ERRO]: {trimester}//{error}")

        return data_buffer

    def load_to_s3(self, data_list):
        if data_list:
            logging.info("Consolidando dados...")
            final_df = pd.concat(data_list, ignore_index=True)
            final_df.drop_duplicates(inplace=True)

            csv_buffer = StringIO()
            final_df.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8")

            s3_client = boto3.client("s3")
            bucket_name = "joao-ans-raw-data"

            try:
                logging.info(f"Iniciando upload para o S3 em {bucket_name}...")
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=self.final_filename,
                    Body=csv_buffer.getvalue()
                )
                logging.info(f"Arquivo {self.final_filename} salvo na nuvem.")
                return True
            except Exception as error:
                logging.error(f"[ERRO]: {error}")
                return False
        else:
            logging.warning("Nenhum dado foi coletado.")
            return False

    def implement(self):
        init = time.time()
        data = self.extract_and_transform()
        sucess = self.load_to_s3(data)
        end = time.time()
        logging.info(f"Executou em  {end - init:.2f} segundos")
        return sucess

def lambda_handler(event, context):
    etl = ETLEventsANS()
    status = etl.implement()

    if status:
        return {'statusCode': 200, 'body': 'ETL Executado com Sucesso!'}
    else:
        return {'statusCode': 500, 'body': 'Erro na execução do ETL.'}

if __name__ == '__main__':
    lambda_handler(None, None)