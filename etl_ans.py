import os
import requests
import zipfile
import pandas as pd
import io
import time
import logging

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

OUT_DIR = "dados_brutos"

FINAL_FILE = "consolidado_despesas.csv"

TRIMESTER = ["2024/01", "2024/02", "2024/03"]

def downloandANDprocess():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    save_data = []

    print (f"ETL da ANS: ")

    for trimester in TRIMESTER:
        year, tri = trimester.split("/")
        tri_number = str(int(tri))

        file_name_zip = f"{tri_number}T{year}.zip"
        full_url = f"{BASE_URL}{year}/{file_name_zip}"

        print(f"URL: {full_url}")

        try:
            response = requests.get(full_url, stream=True)

            if response.status_code == 200:
                print("Download OK")

                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    csv_files = []
                    for f in z.namelist():
                        if f.lower().endswith(".csv"):
                            csv_files.append(f)

                    for file in csv_files:
                        if "despesa" in file.lower() or "evento" in file.lower():
                            print(f"Lendo: {file}")

                            with z.open(file) as f:

                                try:
                                    df = pd.read_csv(f, sep=";", encoding="latin1", dtype=str)
                                except Exception:
                                    f.seek(0)
                                    df = pd.read_csv(f, sep=";", encoding="utf-8", dtype=str)

                                df.columns = [column.strip().upper() for column in df.columns]

                                df["TRIMESTRE_REF"] = f"{tri}T{year}"

                                save_data.append(df)
        except Exception as error:
            print(f"ERRO: {error}")