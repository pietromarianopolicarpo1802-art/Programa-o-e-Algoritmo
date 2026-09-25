import json
import csv
import shutil
from datetime import datetime
import os


ARQUIVO_DADOS = "lanchonete_dados.json"
ARQUIVO_BACKUP = "lanchonete_dados_backup.json"
ARQUIVO_CSV = "relatorio_vendas.csv"


def carregar_dados():
    """
    Carrega os dados do arquivo JSON.
    Se o arquivo não existir, cria um novo.
    """

    if not os.path.exists(ARQUIVO_DADOS):
        dados = {
            "products": [],
            "orders": []
        }

        salvar_dados(dados)
        return dados

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if "products" not in dados:
            dados["products"] = []

        if "orders" not in dados:
            dados["orders"] = []

        return dados

    except json.JSONDecodeError:
        print("\nERRO: O arquivo JSON está inválido.")
        print("Um novo arquivo será criado.")

        dados = {
            "products": [],
            "orders": []
        }

        salvar_dados(dados)

        return dados


def salvar_dados(dados):
    """
    Salva os dados no arquivo JSON.
    """

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def ler_inteiro(mensagem):
    """
    Lê um número inteiro maior ou igual a zero.
    """

    while True:
        try:
            valor = int(input(mensagem))

            if valor < 0:
                print("Digite um número maior ou igual a zero.")
            else:
                return valor

        except ValueError:
            print("Digite apenas números inteiros.")


def ler_quantidade(mensagem):
    """
    Lê uma quantidade maior que zero.
    """

    while True:
        try:
            valor = int(input(mensagem))

            if valor <= 0:
                print("A quantidade deve ser maior que zero.")
            else:
                return valor

        except ValueError:
            print("Digite uma quantidade válida.")


def ler_preco(mensagem):
    """
    Lê um preço válido.
    Aceita tanto ponto quanto vírgula.
    """

    while True:
        try:
            valor = input(mensagem).replace(",", ".")
            preco = float(valor)

            if preco <= 0:
                print("O preço deve ser maior que zero.")
            else:
                return round(preco, 2)

        except ValueError:
            print("Digite um preço válido.")


def cadastrar_produto(dados):
    print("\n" + "=" * 50)
    print("CADASTRAR PRODUTO")
    print("=" * 50)

    codigo = input("Código do produto: ").strip()

    if codigo == "":
        print("O código não pode ficar vazio.")
        return

    # Verificar código repetido
    for produto in dados["products"]:
        if produto["code"] == codigo:
            print("Já existe um produto com esse código.")
            return

    nome = input("Nome do produto: ").strip()

    if nome == "":
        print("O nome do produto não pode ficar vazio.")
        return

    preco = ler_preco("Preço: R$ ")
    estoque = ler_inteiro("Quantidade em estoque: ")

    produto = {
        "code": codigo,
        "name": nome,
        "price": preco,
        "stock": estoque
    }

    dados["products"].append(produto)

    salvar_dados(dados)

    print("\nProduto cadastrado com sucesso!")


def listar_produtos(dados):
    print("\n" + "=" * 70)
    print("LISTA DE PRODUTOS")
    print("=" * 70)

    if len(dados["products"]) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in dados["products"]:
        print(
            f"Código: {produto['code']}\n"
            f"Nome: {produto['name']}\n"
            f"Preço: R$ {produto['price']:.2f}\n"
            f"Estoque: {produto['stock']}"
        )
        print("-" * 70)


def pesquisar_produto(dados):
    print("\n" + "=" * 50)
    print("PESQUISAR PRODUTO")
    print("=" * 50)

    pesquisa = input("Digite o nome do produto: ").strip().lower()

    if pesquisa == "":
        print("Digite um nome para pesquisar.")
        return

    encontrados = []

    for produto in dados["products"]:
        if pesquisa in produto["name"].lower():
            encontrados.append(produto)

    if len(encontrados) == 0:
        print("Nenhum produto encontrado.")
        return

    print("\nProdutos encontrados:")

    for produto in encontrados:
        print(
            f"\nCódigo: {produto['code']}"
            f"\nNome: {produto['name']}"
            f"\nPreço: R$ {produto['price']:.2f}"
            f"\nEstoque: {produto['stock']}"
        )


def alterar_preco(dados):
    print("\n" + "=" * 50)
    print("ALTERAR PREÇO")
    print("=" * 50)

    codigo = input("Digite o código do produto: ").strip()

    for produto in dados["products"]:

        if produto["code"] == codigo:

            print(f"Produto: {produto['name']}")
            print(f"Preço atual: R$ {produto['price']:.2f}")

            novo_preco = ler_preco("Novo preço: R$ ")

            produto["price"] = novo_preco

            salvar_dados(dados)

            print("\nPreço alterado com sucesso!")

            return

    print("Produto não encontrado.")


def remover_produto(dados):
    print("\n" + "=" * 50)
    print("REMOVER PRODUTO")
    print("=" * 50)

    codigo = input("Digite o código do produto: ").strip()

    for produto in dados["products"]:

        if produto["code"] == codigo:

            print(f"\nProduto encontrado: {produto['name']}")

            confirmacao = input(
                "Deseja realmente remover? (S/N): "
            ).strip().lower()

            if confirmacao == "s":

                dados["products"].remove(produto)

                salvar_dados(dados)

                print("\nProduto removido com sucesso!")

            else:
                print("Operação cancelada.")

            return

    print("Produto não encontrado.")


def fazer_pedido(dados):
    print("\n" + "=" * 50)
    print("FAZER PEDIDO")
    print("=" * 50)

    if len(dados["products"]) == 0:
        print("Não existem produtos cadastrados.")
        return

    cliente = input("Nome do cliente: ").strip()

    if cliente == "":
        print("O nome do cliente não pode ficar vazio.")
        return

    listar_produtos(dados)

    codigo = input(
        "\nDigite o código do produto: "
    ).strip()

    produto_encontrado = None

    for produto in dados["products"]:

        if produto["code"] == codigo:
            produto_encontrado = produto
            break

    if produto_encontrado is None:
        print("Produto não encontrado.")
        return

    if produto_encontrado["stock"] <= 0:
        print("Esse produto está sem estoque.")
        return

    quantidade = ler_quantidade(
        "Digite a quantidade desejada: "
    )

    if quantidade > produto_encontrado["stock"]:

        print(
            f"Estoque insuficiente.\n"
            f"Disponível: {produto_encontrado['stock']}"
        )

        return

    total = round(
        produto_encontrado["price"] * quantidade,
        2
    )

    produto_encontrado["stock"] -= quantidade

    pedido = {
        "customer_name": cliente,
        "product_code": produto_encontrado["code"],
        "product_name": produto_encontrado["name"],
        "quantity": quantidade,
        "total": total,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    dados["orders"].append(pedido)

    salvar_dados(dados)

    print("\n" + "=" * 50)
    print("PEDIDO REALIZADO COM SUCESSO")
    print("=" * 50)

    print(f"Cliente: {cliente}")
    print(f"Produto: {produto_encontrado['name']}")
    print(f"Quantidade: {quantidade}")
    print(f"Valor total: R$ {total:.2f}")
    print(
        f"Estoque restante: "
        f"{produto_encontrado['stock']}"
    )


def ver_pedidos(dados):
    print("\n" + "=" * 60)
    print("PEDIDOS REALIZADOS")
    print("=" * 60)

    if len(dados["orders"]) == 0:
        print("Nenhum pedido realizado.")
        return

    for numero, pedido in enumerate(
        dados["orders"],
        start=1
    ):

        print(f"\nPEDIDO #{numero}")
        print(f"Cliente: {pedido['customer_name']}")
        print(f"Produto: {pedido['product_name']}")
        print(f"Código: {pedido['product_code']}")
        print(f"Quantidade: {pedido['quantity']}")
        print(f"Total: R$ {pedido['total']:.2f}")

        if "date" in pedido:
            print(f"Data: {pedido['date']}")

        print("-" * 60)



def relatorio_vendas(dados):
    print("\n" + "=" * 60)
    print("RELATÓRIO DE VENDAS")
    print("=" * 60)

    if len(dados["orders"]) == 0:
        print("Nenhuma venda realizada.")
        return

    total = 0
    quantidade = 0

    for pedido in dados["orders"]:
        total += pedido["total"]
        quantidade += pedido["quantity"]

    print(f"Total de pedidos: {len(dados['orders'])}")
    print(f"Itens vendidos: {quantidade}")
    print(f"Total vendido: R$ {total:.2f}")


def produto_mais_vendido(dados):
    print("\n" + "=" * 60)
    print("PRODUTO MAIS VENDIDO")
    print("=" * 60)

    if len(dados["orders"]) == 0:
        print("Nenhuma venda realizada.")
        return

    vendas = {}

    for pedido in dados["orders"]:

        codigo = pedido["product_code"]
        nome = pedido["product_name"]
        quantidade = pedido["quantity"]

        if codigo not in vendas:
            vendas[codigo] = {
                "name": nome,
                "quantity": 0
            }

        vendas[codigo]["quantity"] += quantidade

    mais_vendido = max(
        vendas.values(),
        key=lambda item: item["quantity"]
    )

    print(f"Produto: {mais_vendido['name']}")
    print(
        f"Quantidade vendida: "
        f"{mais_vendido['quantity']}"
    )


def total_vendido_no_dia(dados):
    print("\n" + "=" * 60)
    print("TOTAL VENDIDO NO DIA")
    print("=" * 60)

    hoje = datetime.now().strftime("%Y-%m-%d")

    total = 0

    for pedido in dados["orders"]:

        data = pedido.get("date", "")

        if data.startswith(hoje):
            total += pedido["total"]

    print(f"Data: {hoje}")
    print(f"Total vendido hoje: R$ {total:.2f}")


def exportar_csv(dados):
    print("\n" + "=" * 60)
    print("EXPORTAR RELATÓRIO PARA CSV")
    print("=" * 60)

    if len(dados["orders"]) == 0:
        print("Não existem vendas para exportar.")
        return

    with open(
        ARQUIVO_CSV,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        campos = [
            "cliente",
            "codigo_produto",
            "produto",
            "quantidade",
            "total",
            "data"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()

        for pedido in dados["orders"]:

            escritor.writerow({
                "cliente": pedido["customer_name"],
                "codigo_produto": pedido["product_code"],
                "produto": pedido["product_name"],
                "quantidade": pedido["quantity"],
                "total": pedido["total"],
                "data": pedido.get("date", "")
            })

    print(
        f"Relatório criado com sucesso: "
        f"{ARQUIVO_CSV}"
    )


def criar_backup():
    print("\n" + "=" * 60)
    print("BACKUP DOS DADOS")
    print("=" * 60)

    if not os.path.exists(ARQUIVO_DADOS):
        print("Arquivo de dados não encontrado.")
        return

    try:

        shutil.copy2(
            ARQUIVO_DADOS,
            ARQUIVO_BACKUP
        )

        print(
            f"Backup criado com sucesso!\n"
            f"Arquivo: {ARQUIVO_BACKUP}"
        )

    except Exception as erro:

        print(
            f"Erro ao criar backup: {erro}"
        )


def mostrar_menu():

    print("\n")
    print("=" * 60)
    print("             SISTEMA PARA LANCHONETE")
    print("                       v2.0")
    print("=" * 60)

    print("1  - Cadastrar produto")
    print("2  - Listar produtos")
    print("3  - Alterar preço")
    print("4  - Remover produto")
    print("5  - Pesquisar produto")
    print("6  - Fazer pedido")
    print("7  - Ver pedidos realizados")
    print("8  - Relatório de vendas")
    print("9  - Produto mais vendido")
    print("10 - Total vendido no dia")
    print("11 - Exportar relatório para CSV")
    print("12 - Criar backup do JSON")
    print("0  - Sair")

    print("=" * 60)


def main():

    dados = carregar_dados()

    print("\n")
    print("=" * 60)
    print("🍔 BEM-VINDO AO SISTEMA DA LANCHONETE 🍔")
    print("=" * 60)

    while True:

        mostrar_menu()

        opcao = input(
            "Digite uma opção: "
        ).strip()

        if opcao == "1":

            cadastrar_produto(dados)

        elif opcao == "2":

            listar_produtos(dados)

        elif opcao == "3":

            alterar_preco(dados)

        elif opcao == "4":

            remover_produto(dados)

        elif opcao == "5":

            pesquisar_produto(dados)

        elif opcao == "6":

            fazer_pedido(dados)

        elif opcao == "7":

            ver_pedidos(dados)

        elif opcao == "8":

            relatorio_vendas(dados)

        elif opcao == "9":

            produto_mais_vendido(dados)

        elif opcao == "10":

            total_vendido_no_dia(dados)

        elif opcao == "11":

            exportar_csv(dados)

        elif opcao == "12":

            criar_backup()

        elif opcao == "0":

            print("\nSistema encerrado.")
            print("Obrigado por utilizar o sistema!")

            break

        else:

            print(
                "\nOpção inválida!"
                "\nEscolha uma opção disponível."
            )


if __name__ == "__main__":
    main()