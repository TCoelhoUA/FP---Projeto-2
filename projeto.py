# Módulos importados
import requests
import time
import json
import math
from prettytable import PrettyTable

# Na pasta do projeto há um ficheiro "external_files" que tem documentos de texto para evitar poluir o código principal. Todas as variáveis que terminarem em "_python_files" vêm desse ficheiro externo.
from external_files import categories_python_file, welcome, menu, program_details

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

    choice = None

    while True:
        print(welcome)
        choice = input(menu+"\n                                                                                               Comando: ").strip()
    
        while choice not in ("1", "2", "3"):
            choice = input(menu+"\n                                                                                         \u26A0 Comando inválido! \u26A0\n                                                                                               Comando: ").strip()

        if choice == "1":
            print(program_details)
            input("\n                                                                                Pressiona uma tecla para voltar ao menu...")
        
        if choice == "2":
            print("")
            for item in categories_python_file:
                print("                                                                          \u2022 "+item)
            input("\n                                                                                Pressiona uma tecla para voltar ao menu...")
        if choice == "3":
            break

    # Este while server apenas para garantir que as variáveis lon, lat e radius são convertíveis para float sem dar erro.
    while not (is_number(lon) and is_number(lat) and is_number(radius)):
        if not is_number(lon):
            print("\u26A0 A longitude introduza é inválida! \u26A0")
            lon = input("Insira a sua longitude: ")
        if not is_number(lat):
            print("\u26A0 A latitude introduza é inválida! \u26A0")
            lat = input("Insira a sua latitude: ")
        if not is_number(radius):
            print("\u26A0 O raio introduzido é inválido! \u26A0")
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
    url = "https://api.geoapify.com/v2/places?categories=service&bias=proximity:-8.483349,40.786700&apiKey=041fa32a7f874d2594bd27b29a1a39fd&filter=circle:-8.483349,40.786700,1000"

    # A variável resp resulta da resposta da API conforme os dados introduzidos (categories, filter, lon, lat, radius, etc...)
    resp = requests.get(f"{url}")

    #
    #
    #
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    print("resp.status_code:", resp.status_code)  # deve ser 200
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    #
    #
    #

    # A variável data_dict resulta da transformação da string devolvida pela API em uma estrutura de dados do Python, neste caso, um dicionário.
    data_dict = json.loads(resp.text)

    # A variável table é criada através de uma função de um módulo. Como parâmetros, introduzi o que queria que aparecesse na primeira linha/topo da tabela.
    table = PrettyTable(["Nome", "\u2690 País", "\U0001F3DB  Distrito", "\U0001F3E2 Concelho", "\U0001F3D8  Freguesia", "\U0001F79C  Localização", "Distância"]) 

    # Este ciclo for percorre as propriedades da API de forma a encontrar o que quer e adicionar isso a uma tabela através do módulo "prettytable".
    total_attractions = 0
    average_distance = 0

    # Este for itera quantas vezes o número de atrações que forem devolvidas pela API.
    for i in range(len(data_dict["features"])):
        properties = data_dict["features"][i]["properties"]

        # Se a atração i tiver a propriedade "name", então o programa adiciona as respetivas informações (predefinidas como None), caso contrário, ignora.
        if "name" in properties:
            name = properties["name"]
            properties_dict = {"country": None, "county": None, "city": None, "district": None, "lat": None, "lon": None, "distance": None}
            total_attractions += 1

            # Este ciclo for verifica se, por cada propriedade, existe essa informação no ficheiro JSON recebido. Se sim, então o valor associado à key do dicionário fica o que vem na API, caso contrário fica "Sem informação".
            for item in ("country", "county", "city", "district", "lat", "lon", "distance"):
                if item not in properties:
                    properties_dict[item] = "Sem informação"
                else:
                    properties_dict[item] = properties[item]

            average_distance += float(properties_dict["distance"])

            # Depois de organizar a informação toda, então o passo seguinte é formatar essa informação numa tabela adicionando uma linha com informações e uma linha vazia.
            table.add_row([name, properties_dict["country"], properties_dict["county"], properties_dict["city"], properties_dict["district"], f'Lat: {properties["lat"]} | Lon: {properties["lon"]}', f'Distância: {properties_dict["distance"]}m'])
            table.add_row(["","","","","","",""])

    # Visto que durante o ciclo for fomos adicionando todas as distâncias, no fim temos de dividir pelo número de atrações.
    average_distance = average_distance/total_attractions

    # Elimina a última linha da tabela de forma a que não fique uma linha vazia (uma vez que o ciclo for anterior adicionava uma linha vazia após cada elemento).
    table.del_row(len(table._rows)-1)
    print(table)
    print(f"""\nNúmero total de atrações detectadas: {total_attractions}\nDistância média das atrações: {average_distance}m""")
main()