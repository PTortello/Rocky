# Pedro Tortello - 21/08/2020


import json
from operator import itemgetter


# Corrige os caracteres modificados
def name_fixer(name):
    modified = {"æ": "a", "¢": "c", "ø": "o", "ß": "b"}
    for character in name:
        if character in modified:
            name = name.replace(character, modified.get(character))
    return name


# Lendo o arquivo JSON
with open("broken-database.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Recuperando os dados corrompidos
for product in data:
    product["name"] = name_fixer(product["name"])
    product["price"] = float(product["price"])
    if not product.get("quantity"):
        product["quantity"] = 0

# Exportando o arquivo JSON corrigido
with open("saida.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


### Validação do banco de dados corrigido ###

# Ordenando os produtos por categoria e id em ordem crescente
sortedData = sorted(data, key=itemgetter("category", "id"))

# Imprime a lista ordenada, formatando conforme o template
template = "{category:20} | {id:10} | {name:50}"
for product in sortedData:
    product["id"] = str(product["id"])
    print(template.format(**product))
print()

# Calculando os totais em estoque para cada categoria
totals = {}
for product in sortedData:
    key = product["category"]
    prodTotal = product["quantity"] * product["price"]
    try:
        totals[key] += prodTotal
    except KeyError:
        totals[key] = prodTotal

# Imprime os totais em estoque por categoria
for product in totals:
    print(f"Valor total de {product}: R$ " + "%.2f" % totals[product])
