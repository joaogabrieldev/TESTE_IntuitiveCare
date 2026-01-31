import unittest
import pandas as pd
from io import StringIO

class CleanDataTest(unittest.TestCase):
    def standart_columns_test(self):
        csv_data = StringIO("Data Evento; Valor Despesa \n2024-01-01;100")
        df = pd.read_csv(csv_data, sep=";")

        df.columns = [c.strip().upper() for c in df.columns]

        self.assertIn("DATA EVENTO", df.columns)
        self.assertIn("VALOR DESPESA", df.columns)
        self.assertNotIn("Data Evento", df.columns)

if __name__ == '__main__':
    unittest.main()