# Módulos importados
import requests
import time

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

    url = f"https://api.geoapify.com/v2/places?categories={categories}" + "&apiKey=041fa32a7f874d2594bd27b29a1a39fd" + f"&filter=circle:{lon},{lat},{radius}"

    resp = requests.get(f"{url}")
    print("resp.status_code:", resp.status_code)  # deve ser 200

    data_dict = resp.json()

    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    print("resp.text:\n", resp.text,"\n\n\n\n\n\n\n\n\n\n") # Imprime tudo o que a API devolve.
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    for item in data_dict:
        print(data_dict.get(features.get(city)))

main()