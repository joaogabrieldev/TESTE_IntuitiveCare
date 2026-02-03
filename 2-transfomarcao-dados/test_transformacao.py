import unittest

from transformacao_dados import DataTransformer


class TestTransformacao(unittest.TestCase):

    def setUp(self):
        self.transformer = DataTransformer()

    def test_cnpj_valido(self):

        cnpj_valido = "06.990.590/0001-23"
        resultado = self.transformer.validate_cnpj(cnpj_valido)
        self.assertTrue(resultado, f"Deveria aceitar {cnpj_valido} como válido")

    def test_cnpj_invalido_digito(self):
        cnpj_errado = "06.990.590/0001-00"
        self.assertFalse(self.transformer.validate_cnpj(cnpj_errado))

    def test_cnpj_invalido_tamanho(self):
        self.assertFalse(self.transformer.validate_cnpj("12345"))
        self.assertFalse(self.transformer.validate_cnpj("1122233300018199999"))

    def test_cnpj_numeros_iguais(self):
        self.assertFalse(self.transformer.validate_cnpj("00.000.000/0000-00"))
        self.assertFalse(self.transformer.validate_cnpj("11.111.111/1111-11"))

    def test_limpeza_formatacao(self):
        cnpj_sujo = "06.990.590/0001-23"
        self.assertTrue(self.transformer.validate_cnpj(cnpj_sujo))

        cnpj_limpo = "06990590000123"
        self.assertTrue(self.transformer.validate_cnpj(cnpj_limpo))


if __name__ == '__main__':
    unittest.main()