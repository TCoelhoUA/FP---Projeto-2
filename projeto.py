# Módulos importados
import requests
import time
import json
from prettytable import PrettyTable

# Na pasta do projeto há um ficheiro "external_files" que tem documentos de texto para evitar poluir o código principal. Todas as variáveis que terminarem em "_python_files" vêm desse ficheiro externo.
from external_files import categories_python_file

# Esta função espera "s" segundos antes de executar a linha de código seguinte (esta função apenas serve para propósitos estéticos e de interatividade para o programa)
def wait(s):
    time.sleep(s)

# Esta função verifica se uma string é um número ou não (também funciona para número negativos, ao contrário da função ".isdigit()")
def is_number(number):
    return number.lstrip("-").isdigit()
def restart():
    wait(1)
    print("Reiniciando programa...\n")
    wait(3)
    main()

def main():
    #lon = input("Insira a sua longitude: ")
    #lat = input("Insira a sua latitude: ")
    #radius = input("Insira o raio: ")

    lon = "-8"
    lat = "40"
    radius = "5000"

    # Este while server apenas para garantir que as variáveis lon, lat e radius são convertíveis para float sem dar erro.
    while not (is_number(lon) and is_number(lat) and is_number(radius)):
        if not is_number(lon):
            print("⚠ A longitude introduza é inválida! ⚠")
            lon = input("Insira a sua longitude: ")
        if not is_number(lat):
            print("⚠ A latitude introduza é inválida! ⚠")
            lat = input("Insira a sua latitude: ")
        if not is_number(radius):
            print("⚠ O raio introduzido é inválido! ⚠")
            radius = input("Insira o raio: ")

    float(lon)
    float(lat)
    float(radius)

    '''
    appended_category = input("Insira as suas categorias de interesse (termine inserindo um input vazio)\n\nCategoria 1: ").strip().lower()
    
    if appended_category not in categories_python_file:
        while appended_category != "":
            appended_category = input("⚠ Tem de escolher uma categoria válida! ⚠\n\nCategoria 1: ").lower()

    categories = appended_category
    # Enquanto a "appended_category" não for vazia, será pedido ao utilizador que adicione uma nova categoria. O ciclo acaba quando appended_category for igual a "".
    i = 1
    while appended_category != "":
        i += 1
        appended_category = input(f"Categoria {i}: ").strip().lower()
        if appended_category not in categories_python_file:
            while appended_category != "":
                appended_category = input(f"⚠ Tem de escolher uma categoria válida! ⚠\n\nCategoria {i}: ").lower()
        if appended_category != "":
            categories += ","+appended_category

    if categories == "":
        print("⚠ Tem de escolher pelo menos um categoria! ⚠\n")
        restart()
    '''

    categories = "accommodation,catering"

    #url = f"https://api.geoapify.com/v2/places?categories={categories}" + "&apiKey=041fa32a7f874d2594bd27b29a1a39fd" + f"&filter=circle:{lon},{lat},{radius}"
    url = "https://api.geoapify.com/v2/places?categories=catering,accommodation&apiKey=041fa32a7f874d2594bd27b29a1a39fd&filter=circle:-9.14,38.72,5000"

    # A variável resp resulta da resposta da API conforme os dados introduzidos (categories, filter, lon, lat, radius, etc...)
    resp = requests.get(f"{url}")

    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    print("resp.status_code:", resp.status_code)  # deve ser 200
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR

    # A variável data_dict resulta da transformação da string devolvida pela API em uma estrutura de dados do Python, neste caso, um dicionário.
    data_dict = json.loads(resp.text)

    '''
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    print("resp.text:\n", resp.text,"\n\n\n\n\n\n\n\n\n\n") # Imprime tudo o que a API devolve.
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    
    Distrito (county), Concelho (city), Freguesia (district)
    '''
    table = PrettyTable(["Nome", "País", "Distrito", "Concelho", "Freguesia", "Localização", "Distância"]) 

    # Este ciclo for percorre as propriedades da API de forma a encontrar o que quer e adicionar isso a uma tabela através do módulo "prettytable".
    for i in range(len(data_dict["features"])):
        properties = data_dict["features"][i]["properties"]
        # Se o elemento i tiver a propriedade "name", então o programa adiciona as respetivas informações, caso contrário, ignora.
        if "name" in properties:
            name = properties["name"]
            properties_dict = {"country": None, "county": None, "city": None, "district": None, "lat": None, "lon": None}
            for item in ("country", "county", "city", "district", "lat", "lon"):
                if item not in properties:
                    properties_dict[item] = "Sem informação"
                else:
                    properties_dict[item] = properties[item]

            table.add_row([name, properties_dict["country"], properties_dict["county"], properties_dict["city"], properties_dict["district"], f'Lat: {properties["lat"]} | Lon: {properties["lon"]}', 'Distância'])
            table.add_row(["","","","","","",""])

    # Elimina a última linha da tabela de forma a que não fique uma linha vazia (uma vez que o ciclo for anterior adicionava uma linha vazia após cada elemento).
    table.del_row(len(table._rows)-1)
    print(table)
main()