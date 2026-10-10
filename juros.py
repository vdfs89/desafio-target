"""Desafio 3 - Juros por atraso.

Premissa: taxa de 2,5% AO DIA, juros SIMPLES sobre o valor original,
contados pelos dias corridos entre o vencimento e hoje. Sem atraso = zero.
O enunciado fala em "multa de 2,5% ao dia" e pede "juros"; adotei
juros simples (valor * 2,5% * dias). Há opção de composto (--composto).
"""
import argparse
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

from comissao import brl

TAXA_DIA = Decimal("0.025")
CENTAVO = Decimal("0.01")


def dias_atraso(vencimento: date, hoje: date = None) -> int:
    hoje = hoje or date.today()
    return max((hoje - vencimento).days, 0)


def calcular_juros(valor, vencimento: date, hoje: date = None, composto=False) -> Decimal:
    valor = Decimal(str(valor))
    if valor < 0:
        raise ValueError("Valor não pode ser negativo.")
    dias = dias_atraso(vencimento, hoje)
    if composto:
        juros = valor * ((1 + TAXA_DIA) ** dias - 1)
    else:
        juros = valor * TAXA_DIA * dias
    return juros.quantize(CENTAVO, ROUND_HALF_UP)


def main():
    ap = argparse.ArgumentParser(description="Calcula juros de 2,5% ao dia sobre atraso.")
    ap.add_argument("valor", help="valor original, ex.: 1000.00")
    ap.add_argument("vencimento", help="data de vencimento DD/MM/AAAA")
    ap.add_argument("--composto", action="store_true", help="usa juros compostos")
    a = ap.parse_args()
    venc = datetime.strptime(a.vencimento, "%d/%m/%Y").date()
    dias = dias_atraso(venc)
    j = calcular_juros(a.valor, venc, composto=a.composto)
    v = Decimal(a.valor)
    print(f"Dias em atraso: {dias}\nJuros: {brl(j)}\nTotal: {brl((v + j).quantize(CENTAVO))}")


if __name__ == "__main__":
    main()
