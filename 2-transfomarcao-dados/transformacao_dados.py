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
        self.output_file = os.path.join("dados_brutos", "despesas_agregadas.csv")
        self.zip_filename = " Teste_João-Gabriel.zip"
        self.cadastral_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_Cadop.csv"

    def validate_cnpj(self, cnpj):
        cnpj_filtered = "".join(digito for digito in str(cnpj) if digito.isdigit())

        if len(cnpj_filtered) != 14 or cnpj_filtered == cnpj_filtered[0] * 14:
            return False

        def calcular_digito(parte_cnpj, pesos):
            soma_produtos = sum(int(digito) * peso for digito, peso in zip(parte_cnpj, pesos))

            resto = soma_produtos % 11
            return 0 if resto < 2 else 11 - resto

        pesos_primeiro_digito = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos_segundo_digito = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        primeiro_digito = calcular_digito(cnpj_filtered[:12], pesos_primeiro_digito)

        segundo_digito = calcular_digito(cnpj_filtered[:13], pesos_segundo_digito)

        return cnpj_filtered[-2:] == f"{primeiro_digito}{segundo_digito}"

    def load_data(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Arquivo {self.input_file} não encontrado.")

        logging.info("Carregando dados...")
        df = pd.read_csv(self.input_file, sep=";", encoding="utf-8", dtype=str)
        df.columns = [column.strip().upper() for column in df.columns]

        col_desc = [c for c in df.columns if "DESCRICAO" in c or "CONTA" in c][-1]

        df = df[df[col_desc].str.contains("EVENTO|SINISTRO|DESPESA", case=False, na=False)]

        logging.info(f"Dados filtrados carregados: {len(df)} linhas.")
        return df

    def get_cadastral_data(self):
        csv_path = os.path.join("dados_brutos", "Relatorio_cadop.csv")
        logging.info(f"Lendo cadastro local: {csv_path}")

        if not os.path.exists(csv_path):
            logging.error("Arquivo Relatorio_Cadop.csv não encontrado!")
            return None

        try:
            df_cadastral = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str)
            df_cadastral.columns = [column.strip().upper() for column in df_cadastral.columns]
            return df_cadastral

        except Exception as error:
            logging.error(f"ERRO: {error}")
            return None

    def process(self):

        df_accounting = self.load_data()
        df_cadastral = self.get_cadastral_data()

        if df_cadastral is None:
            logging.error("[ERRO]: Cadastro não carregado.")
            return

        col_register_accounting = [column for column in df_accounting.columns if "REG" in column and "ANS" in column][0]

        logging.info("Identificando colunas de cruzamento...")

        if "REGISTRO_OPERADORA" in df_cadastral.columns:
            col_register_cadastral = "REGISTRO_OPERADORA"
        else:

            cols_possiveis = [column for column in df_cadastral.columns if "REGISTRO" in column and "DATA" not in column]
            if cols_possiveis:
                col_register_cadastral = cols_possiveis[0]
            else:
                logging.error("Coluna de registro não encontrada")
                logging.error(f"Colunas disponíveis: {df_cadastral.columns.tolist()}")
                return

        logging.info("Cruzando dados...")

        df_merged = pd.merge(
            df_accounting,
            df_cadastral[[col_register_cadastral, 'CNPJ', 'RAZAO_SOCIAL', 'UF']],
            left_on=col_register_accounting,
            right_on=col_register_cadastral,
            how="inner"
        )

        col_value = [column for column in df_merged.columns if "VALOR" in column or "SALDO" in column][0]
        df_merged[col_value] = df_merged[col_value].str.replace(",", ".").astype(float)

        df_merged = df_merged[df_merged[col_value] > 0]

        df_merged["CNPJ_LIMPO"] = df_merged["CNPJ"].str.replace(r"\D", "", regex=True)
        df_merged['CNPJ_VALIDO'] = df_merged['CNPJ_LIMPO'].apply(self.validate_cnpj)

        df_final = df_merged[df_merged["CNPJ_VALIDO"] == True].copy()

        logging.info("Realizando cálculos...")
        df_agg = df_final.groupby(['RAZAO_SOCIAL', 'UF'])[col_value].agg(
            TOTAL_DESPESAS="sum",
            MEDIA_TRIMESTRAL="mean",
            DESVIO_PADRAO="std"
        ).reset_index().sort_values(by="TOTAL_DESPESAS", ascending=False)

        cols_num = ['TOTAL_DESPESAS', 'MEDIA_TRIMESTRAL', 'DESVIO_PADRAO']
        df_agg[cols_num] = df_agg[cols_num].round(2)

        df_agg.to_csv(self.output_file, index=False, sep=";", encoding="utf-8-sig", decimal=",")

        with zipfile.ZipFile(self.zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(self.output_file, arcname="despesas_agregadas.csv")

        logging.info(f"Arquivo final gerado: {self.zip_filename}")
        logging.info(f"Local: {os.path.abspath(self.zip_filename)}")

        if df_agg.empty:
            logging.warning("O arquivo final está vazio!")
        else:
            logging.info("\n" + df_agg.head().to_string())

if __name__ == '__main__':
    etl = DataTransformer()
    etl.process()














