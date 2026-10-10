import json, os, sys, tempfile, unittest
from datetime import date
from decimal import Decimal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import comissao, estoque, juros


class TestComissao(unittest.TestCase):
    def test_faixas(self):
        self.assertEqual(comissao.comissao_venda(99.99), 0)
        self.assertEqual(comissao.comissao_venda(100), Decimal("1.00"))
        self.assertEqual(comissao.comissao_venda(499.99), Decimal("4.9999"))
        self.assertEqual(comissao.comissao_venda(500), Decimal("25.00"))

    def test_json_exemplo(self):
        base = os.path.join(os.path.dirname(__file__), "..", "vendas.json")
        with open(base, encoding="utf-8") as f:
            r = comissao.calcular_comissoes(json.load(f)["vendas"])
        self.assertEqual(list(r), ["João Silva", "Maria Souza", "Carlos Oliveira", "Ana Lima"])
        self.assertEqual(r["João Silva"], Decimal("495.68"))


class TestEstoque(unittest.TestCase):
    def setUp(self):
        self.e = estoque.Estoque([{"codigoProduto": 101, "descricaoProduto": "Caneta", "estoque": 10}])

    def test_entrada_saida_e_ids(self):
        m1 = self.e.movimentar(101, "entrada", 5, "Compra")
        m2 = self.e.movimentar(101, "SAIDA", 3, "Venda")
        self.assertEqual((m1["id"], m1["estoqueFinal"]), (1, 15))
        self.assertEqual((m2["id"], m2["estoqueFinal"]), (2, 12))

    def test_erros(self):
        for args in [(999, "ENTRADA", 1, "x"), (101, "SAIDA", 11, "x"),
                     (101, "ENTRADA", 0, "x"), (101, "ENTRADA", 1, " "), (101, "XYZ", 1, "x")]:
            with self.assertRaises(estoque.EstoqueError):
                self.e.movimentar(*args)
        self.assertEqual(self.e.produtos[101]["estoque"], 10)

    def test_persistencia_continua_ids(self):
        self.e.movimentar(101, "ENTRADA", 5, "Compra")
        with tempfile.TemporaryDirectory() as d:
            estado = os.path.join(d, "estado.json")
            self.e.salvar(estado)
            recarregado = estoque.carregar(estado)
        self.assertEqual(recarregado.produtos[101]["estoque"], 15)
        self.assertEqual(recarregado.movimentar(101, "SAIDA", 1, "Venda")["id"], 2)


class TestJuros(unittest.TestCase):
    def test_simples(self):
        self.assertEqual(juros.calcular_juros(1000, date(2026, 10, 1), date(2026, 10, 5)), Decimal("100.00"))

    def test_sem_atraso(self):
        self.assertEqual(juros.calcular_juros(1000, date(2026, 10, 10), date(2026, 10, 5)), Decimal("0.00"))
        self.assertEqual(juros.calcular_juros(1000, date(2026, 10, 5), date(2026, 10, 5)), Decimal("0.00"))

    def test_composto(self):
        self.assertEqual(juros.calcular_juros(1000, date(2026, 10, 1), date(2026, 10, 3), composto=True), Decimal("50.63"))


if __name__ == "__main__":
    unittest.main()
