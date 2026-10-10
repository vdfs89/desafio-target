"""Desafio 1 - Comissão por vendedor.

Regra (por venda):
  valor < 100          -> sem comissão
  100 <= valor < 500   -> 1%
  valor >= 500         -> 5%
"""
import json
import sys
from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def percentual(valor: Decimal) -> Decimal:
    if valor < Decimal("100"):
        return Decimal("0")
    if valor < Decimal("500"):
        return Decimal("0.01")
    return Decimal("0.05")


def comissao_venda(valor) -> Decimal:
    valor = Decimal(str(valor))
    return valor * percentual(valor)


def calcular_comissoes(vendas) -> "OrderedDict[str, Decimal]":
    """Soma a comissão de cada venda e arredonda só no total (centavos)."""
    totais = OrderedDict()
    for venda in vendas:
        nome = venda["vendedor"]
        totais[nome] = totais.get(nome, Decimal("0")) + comissao_venda(venda["valor"])
    return OrderedDict((n, t.quantize(CENTAVO, ROUND_HALF_UP)) for n, t in totais.items())


def brl(valor: Decimal) -> str:
    return "R$ {:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")


def main(caminho="vendas.json"):
    with open(caminho, encoding="utf-8") as f:
        vendas = json.load(f)["vendas"]
    for nome, total in calcular_comissoes(vendas).items():
        print(f"{nome}: {brl(total)}")


if __name__ == "__main__":
    main(*sys.argv[1:2])
