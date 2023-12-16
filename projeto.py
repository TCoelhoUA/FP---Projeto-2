# Módulos importados
import requests
import time
import json
from prettytable import PrettyTable
import csv

# Na pasta do projeto há um ficheiro "external_files" que tem documentos de texto para evitar poluir o código principal. Todas as variáveis que terminarem em "_python_files" vêm desse ficheiro externo.
from external_files import categories_python_file, welcome, menu, program_details

# Esta função espera "s" segundos antes de executar a linha de código seguinte (esta função apenas serve para propósitos estéticos e de interatividade para o programa)
def wait(s):
    time.sleep(s)


# Esta função verifica se uma string é um número ou não (também funciona para número negativos, ao contrário da função ".isdigit()")
def is_number(number):
    return number.lstrip("-").isdigit()


# Esta função serve apenas para "dinamizar" a parte visual do programa quando estiver a ser corrido novamente.
def restart():
    wait(1)
    print("Reiniciando programa...\n")
    wait(3)
    main()


# Nesta função não é contemplada a choice == "3" pois caso isso aconteça, o programa simplesmente continua a correr até chegar onde a choice == "3" levaria.
def menu_options():
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
        return True
        
    if choice == "4":
        exit()


def define_inputs():
    lon = input("Insira a sua longitude.\n=>  ")
    while not is_number(lon.replace(".","")):
        print("\u26A0 A longitude introduza é inválida! \u26A0")
        lon = input("Insira a sua longitude:\n=>  ")

    lat = input("Insira a sua latitude:\n=>  ")
    while not is_number(lat.replace(".","")):
        print("\u26A0 A latitude introduza é inválida! \u26A0")
        lat = input("Insira a sua latitude:\n=>  ")

    radius = input("Quão longe quer viajar? (em km)\n=>  ")
    while not is_number(radius):
        print("\u26A0 A distância introduzida é inválida! \u26A0")
        radius = input("Quão longe quer viajar? (em km)\n=>  ")

    return float(lon), float(lat), float(radius)


def show_main_categories(categories_python_file):
    for category in categories_python_file:
        if "." not in category:
            print(f"\u2022 {category}")


# Esta função verifica se uma category existe apenas 1 vez na lista de categorias, se assim for então não existe mais subcategorias nessa categoria.
def check_subcategory(appended_category, final_category, categories_python_file):
    a = 0
    if appended_category == "":
        return False
    
    for category in categories_python_file:
        '''if appended_category in category:'''
        if final_category in category:
            a += 1
    
    if a > 1:
        return True
    
    return False


# Esta função faz display das categorias disponíveis e também consegue entrar em subcategorias.
def define_categories(categories_python_file):
    i = 1
    categories = ""

    print("Insira as suas categorias de interesse (termine inserindo um input vazio)")
    show_main_categories(categories_python_file)
    appended_category = input("\nCategoria 1:\n=> ").strip().lower()
    
    while appended_category not in categories_python_file:
        if appended_category == "":
            print("\u26A0 Tem de escolher pelo menos uma categoria! \u26A0")
        else:
            print("\u26A0 Tem de escolher uma categoria válida! \u26A0")

        appended_category = input("\nCategoria 1:\n=> ").strip().lower()

    # Este ciclo while verifica se a appended_category não é nula e se ainda existe uma subcategoria.
    while appended_category != "":
        final_category = appended_category
        while check_subcategory(appended_category, final_category, categories_python_file):
            print("\nSubcategorias:")
            subcategories = []
            for category in categories_python_file:
                if final_category in category and final_category != category:
                    min_length = min(len(final_category), len(category))
                    a = 0

                    for char in range(min_length):
                        if final_category[char] == category[char]:
                            a += 1

                    # Esta lista é referente à divisão de uma categoria em subcategoria, por exemplo "a.b.c" fica ["a", "b", "c"] sendo que pouco a pouco se vai percorrendo
                    # a categoria de forma a ir substituindo "a." por "", depois "a.b." por "" até já não haver mais subcategorias
                    subcategory = list(category.replace(final_category+".","").split("."))[0]

                    if a == min_length and subcategory not in subcategories:
                        subcategories.append(subcategory)

            for item in subcategories:
                print(f"\u2022 {item}")

            appended_category = input("\nSubcategoria:\n=> ").lower().strip()

            while appended_category not in subcategories:
                if appended_category != "":
                    appended_category = input("\n\u26A0 Tem de escolher uma subcategoria válida! \u26A0\nSubcategoria:\n=> ")
                else:
                    break

            if appended_category != "":
                final_category += "."+appended_category
            
        if categories == "":
            categories = final_category
        else:
            categories += ","+final_category
        
        # Enquanto a "appended_category" não for vazia, será pedido ao utilizador que adicione uma nova categoria. O ciclo acaba quando appended_category for igual a "".
        i += 1
        show_main_categories(categories_python_file)
        appended_category = input(f"\nCategoria {i}:\n=> ").strip().lower()

        while appended_category not in categories_python_file:
            if appended_category != "":
                appended_category = input(f"\n\u26A0 Tem de escolher uma categoria válida! \u26A0\nCategoria {i}:\n=> ").lower().strip()
            else:
                break
    
    return categories


# Esta função verifica se o "file_name" tem algum caracter inválido ou não.
def has_valid_chars(file_name):
    for char in ("\\", "/", "|", "?", "<", ">", "*", ":", "“"):
        if char in file_name:
            return False
    return True


# Esta função exporta os dados recolhidos pela API para um ficheiro CSV.
def csv_export(total_attractions, data_dict, average_distance):
    file_name = input("Insira um nome para o ficheiro: ")

    while not has_valid_chars(file_name):
        file_name = input("\u26A0 Nome inválido! \u26A0\nO nome do ficheiro não pode incluir nenhum dos seguintes caracteres: \\, /, |, ?, <, >, *, :, “\nInsira um nome para o ficheiro: ")

    with open(f"{file_name}.csv", "w", encoding="utf-8") as fileobj:
        writer = csv.writer(fileobj)
        # Adiciona a primeira linha do ficheiro CSV com os nomes dos dados que serão escritos abaixo.
        writer.writerow(["Nome", "País", "Distrito", "Concelho", "Freguesia", "Latitude", "Longitude", "Distância"])

        # Este ciclo for itera pelas diferentes atrações e por cada uma guarda os seus valores e adiciona uma linha ordenada ao ficheiro CSV.
        for attraction in range(total_attractions+1):
            properties = data_dict["features"][attraction]["properties"]

            # Verifica se a atração tem nome, caso contrário, ignora.
            if "name" in properties:
                name = properties["name"]
                properties_dict = {"name": name, "country": None, "county": None, "city": None, "district": None, "lat": None, "lon": None, "distance": None}

                for item in ("country", "county", "city", "district", "lat", "lon", "distance"):
                    # Se alguma das propriedades não se encontrar na atração, então ficará como "Sem informação".
                    if item not in properties:
                        properties_dict[item] = "Sem informação"
                    else:
                        properties_dict[item] = properties[item]

                # Adiciona uma linha ordenada com as propriedades da atração ao ficheiro CSV.
                writer.writerow([name, properties_dict["country"], properties_dict["county"], properties_dict["city"], properties_dict["district"], f'{properties["lat"]}',f'{properties["lon"]}', f'{properties_dict["distance"]}'])
        
        # Adiciona as estatísticas finais ao ficheiro CSV
        writer.writerow([f"\n--- Estatísticas ---\nTotal de Atrações: {total_attractions}\nDistância média das atrações: {average_distance/1000}km"])

    print(f"O ficheiro {file_name}.csv foi criado na pasta do projeto.")


def store_and_format_data(data_dict):
    total_attractions = 0
    average_distance = 0
    formatted_dict = dict()

    # A variável table é criada através de uma função de um módulo. Como parâmetros, introduzi o que queria que aparecesse na primeira linha/topo da tabela.
    table = PrettyTable(["Nome", "\u2690 País", "\U0001F3DB  Distrito", "\U0001F3E2 Concelho", "\U0001F3D8  Freguesia", "\U0001F79C  Localização", "Distância"])

    for i in range(len(data_dict["features"])):
        properties = data_dict["features"][i]["properties"]

        # Se a atração i tiver a propriedade "name", então o programa adiciona as respetivas informações (predefinidas como None), caso contrário, ignora.
        if "name" in properties:
            name = properties["name"]
            attractions_names = []
            attractions_names.append(name)
            properties_dict = {"name": name, "country": None, "county": None, "city": None, "district": None, "lat": None, "lon": None, "distance": None}
            total_attractions += 1

            # Este ciclo for verifica se, por cada propriedade, existe essa informação no ficheiro JSON recebido. Se sim, então o valor associado à key do dicionário fica o que vem na API, caso contrário fica "Sem informação".
            for item in ("country", "county", "city", "district", "lat", "lon", "distance"):
                if item not in properties:
                    properties_dict[item] = "Sem informação"
                else:
                    properties_dict[item] = properties[item]

            formatted_dict[i] = properties_dict

            average_distance += float(properties_dict["distance"])

            # Depois de organizar a informação toda, então o passo seguinte é formatar essa informação numa tabela adicionando uma linha com informações e uma linha vazia.
            table.add_row([name, properties_dict["country"], properties_dict["county"], properties_dict["city"], properties_dict["district"], f'Lat: {properties["lat"]} | Lon: {properties["lon"]}', f'Distância: {properties_dict["distance"]/1000}km'])
            table.add_row(["","","","","","",""])

    if total_attractions == 0:
        print("\n\u26A0  Não foram encontradas atrações que cumpram os requisitos introduzidos. \u26A0")
        choice = input("Deseja fazer outra pesquisa? (s/n)\n=> ").strip().lower() # Como a variável choice anterior não irá mais ser usada, usámos o mesmo nome para definir este input
        if choice == "s":
            restart()
        else:
            exit()

    # Visto que durante o ciclo for fomos adicionando todas as distâncias, no fim temos de dividir pelo número de atrações.
    average_distance = average_distance/total_attractions
            
    return total_attractions, average_distance, formatted_dict, table


def main():
    print(welcome)

    # Este ciclo while serve para repetir o menu sempre que o utilizador utilizar os comandos "1" e "2".
    while True:
        # A função menu_options() dá return de true se a opção escolhida for "Planear viagem", daí a necessidade de dar break no ciclo while caso essa seja a opção escolhida.
        if menu_options():
            break

    lon, lat, radius = define_inputs()

    print(f"OUTPUT_TESTE: lon = {lon}, lat = {lat}, radius = {radius}")

    categories = define_categories(categories_python_file)

    print("OUTPUT_TESTE: categories = "+categories)

    url = f"https://api.geoapify.com/v2/places?categories={categories}" + f"&bias=proximity:{lon},{lat}" + "&apiKey=041fa32a7f874d2594bd27b29a1a39fd" + f"&filter=circle:{lon},{lat},{radius*1000}"

    # A variável resp resulta da resposta da API conforme os dados introduzidos (categories, filter, lon, lat, radius, etc...)
    resp = requests.get(f"{url}")

    #
    #
    #
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    print(url)
    print("resp.status_code:", resp.status_code)  # deve ser 200
    # REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR REMOVER ANTES DE ENVIAR
    #
    #
    #

    # A variável data_dict resulta da transformação da string devolvida pela API em uma estrutura de dados do Python, neste caso, um dicionário.
    data_dict = json.loads(resp.text)

    total_attractions, average_distance, formatted_dict, table = store_and_format_data(data_dict)

    # Elimina a última linha da tabela de forma a que não fique uma linha vazia (uma vez que o ciclo for anterior adicionava uma linha vazia após cada elemento).
    table.del_row(len(table._rows)-1)
    print(table)

    # A variável statistics_table é criada através de uma função de um módulo. Como parâmetros, introduzi o que queria que aparecesse na primeira linha/topo da tabela.
    statistics_table = PrettyTable(["Estatísticas"])
    statistics_table.add_row([f"No total foram encontradas {total_attractions} atrações."])
    statistics_table.add_row([f"A média da distância dessas atrações é de {average_distance/1000}km"])
    print(statistics_table)

    choice = input("Deseja exportar dados sobre as atrações para CSV? (s/n)\n=> ").strip().lower()
    if choice == "s":
        csv_export(total_attractions, data_dict, average_distance)

    choice = input("Deseja fazer outra pesquisa? (s/n)\n=> ").strip().lower() # Como a variável choice anterior não irá mais ser usada, usámos o mesmo nome para definir este input
    if choice == "s":
        restart()
    else:
        exit()
    

main()