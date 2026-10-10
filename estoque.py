"""Desafio 2 - Movimentações de estoque (entrada/saída).

Cada movimentação tem id único (sequencial, persistido), tipo/descrição e
devolve a quantidade final do produto. O estado fica em estoque_estado.json
para os ids continuarem únicos entre execuções.
"""
import json
import os

ENTRADA, SAIDA = "ENTRADA", "SAIDA"


class EstoqueError(Exception):
    pass


class Estoque:
    def __init__(self, produtos, movimentacoes=None):
        self.produtos = {p["codigoProduto"]: dict(p) for p in produtos}
        self.movimentacoes = list(movimentacoes or [])
        self._proximo_id = max((m["id"] for m in self.movimentacoes), default=0) + 1

    def movimentar(self, codigo, tipo, quantidade, descricao):
        tipo = tipo.upper()
        if tipo not in (ENTRADA, SAIDA):
            raise EstoqueError("Tipo deve ser ENTRADA ou SAIDA.")
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise EstoqueError("Quantidade deve ser um inteiro positivo.")
        if not descricao or not descricao.strip():
            raise EstoqueError("Informe a descrição da movimentação.")
        produto = self.produtos.get(codigo)
        if produto is None:
            raise EstoqueError(f"Produto {codigo} não encontrado.")
        novo = produto["estoque"] + (quantidade if tipo == ENTRADA else -quantidade)
        if novo < 0:
            raise EstoqueError(
                f"Estoque insuficiente: {produto['estoque']} disponível, saída de {quantidade}."
            )
        produto["estoque"] = novo
        mov = {"id": self._proximo_id, "codigoProduto": codigo, "tipo": tipo,
               "quantidade": quantidade, "descricao": descricao.strip(),
               "estoqueFinal": novo}
        self._proximo_id += 1
        self.movimentacoes.append(mov)
        return mov

    def salvar(self, caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump({"estoque": list(self.produtos.values()),
                       "movimentacoes": self.movimentacoes}, f, ensure_ascii=False, indent=2)


def carregar(estado="estoque_estado.json", base="estoque.json"):
    caminho = estado if os.path.exists(estado) else base
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return Estoque(dados["estoque"], dados.get("movimentacoes"))


def main(estado="estoque_estado.json"):
    est = carregar(estado)
    print("Produtos:")
    for p in est.produtos.values():
        print(f"  {p['codigoProduto']} - {p['descricaoProduto']} (estoque: {p['estoque']})")
    while True:
        cod = input("\nCódigo do produto (vazio para sair): ").strip()
        if not cod:
            break
        try:
            tipo = input("Tipo [ENTRADA/SAIDA]: ")
            qtd = int(input("Quantidade: "))
            desc = input("Descrição da movimentação: ")
            mov = est.movimentar(int(cod), tipo, qtd, desc)
        except (ValueError, EstoqueError) as e:
            print(f"Erro: {e}")
            continue
        est.salvar(estado)
        print(f"Movimentação #{mov['id']} ({mov['tipo']} - {mov['descricao']}). "
              f"Estoque final: {mov['estoqueFinal']}")


if __name__ == "__main__":
    main()
