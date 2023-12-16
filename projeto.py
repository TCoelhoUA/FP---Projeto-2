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

# Esta função verifica se uma string é um número ou não (também funciona para número negativos, ao contrário da função ".isdigit()") (para isso, temporariamente retirou-se qualquer símbolo "-")
def is_number(number):
    return number.lstrip("-").isdigit()

# Esta função serve apenas para "dinamizar" a parte visual do programa quando estiver a ser corrido novamente.
def restart():
    wait(1)
    print("Reiniciando programa...\n")
    wait(3)
    main()

# Esta função dá return de True quando a opção escolhida é "2".
def menu_options():
    choice = input(menu+"\n                                                                                               Comando: ").strip()

    # Enquanto o utilizador não inserir uma opção válida será sempre pedido que introduza uma válida
    while choice not in ("1", "2", "3"):
        choice = input(menu+"\n                                                                                         \u26A0 Comando inválido! \u26A0\n                                                                                               Comando: ").strip()

    # 1 - Como funciona o programa?
    if choice == "1":
        print(program_details)
        input("\n                                                                                Pressiona uma tecla para voltar ao menu...")
    
    # 2- Planear viagem
    if choice == "2":
        return True
    
    # 3- Sair
    if choice == "3":
        exit()

# Esta função é utilizada para validar se os inputs introduzidos são número ou não (para isso, temporariamente retirou-se qualquer símbolo ".")
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

    # Retorna os valores em tipo float
    return float(lon), float(lat), float(radius)

# Esta função é utilizada para mostrar todas as categorias principais.
def show_main_categories(categories_python_file):
    for category in categories_python_file:
        # Se a categoria não contiver o símbolo ".", então é uma categoria principal, logo damos print da categoria.
        if "." not in category:
            print(f"\u2022 {category}")

# Esta função verifica se uma categoria existe apenas 1 vez na lista de categorias, se assim for então não existe mais subcategorias nessa categoria.
def check_subcategory(appended_category, final_category, categories_python_file):
    a = 0
    if appended_category == "":
        return False
    
    for category in categories_python_file:
        if final_category in category:
            a += 1
    
    if a > 1:
        return True
    
    return False

# Esta função vai guardar todas as categorias que o utilizador introduzir dando print das categorias disponíveis e também das subcategorias (se existirem).
def define_categories(categories_python_file):

    '''
    INFORMAÇÃO: Ao longo desta função, categorias e subcategorias serão guardadas na mesma variável (appended_category).
    '''

    i = 1 # Começamos com i = 1, pois, mais à frente, esta variável será usada para mostrar Categoria 2, Categoria 3, etc...
    categories = ""

    print("Insira as suas categorias de interesse (termine inserindo um input vazio)")
    show_main_categories(categories_python_file)

    # Pede a primeira categoria ao utilizador.
    appended_category = input("\nCategoria 1:\n=> ").strip().lower()
    
    # Enquanto a categoria introduzida não estiver na lista de categorias, então ou é uma string vazia ou uma categoria inválida.
    while appended_category not in categories_python_file:
        if appended_category == "":
            print("\u26A0 Tem de escolher pelo menos uma categoria! \u26A0")
        else:
            print("\u26A0 Tem de escolher uma categoria válida! \u26A0")

        # Pede um novo input ao utilizador.
        appended_category = input("\nCategoria 1:\n=> ").strip().lower()

    # Este ciclo while verifica se a appended_category não é nula e se ainda existe uma subcategoria.
    while appended_category != "":
        final_category = appended_category # Começamos por fazer com que a categoria final seja igual à primeira categoria introduzida
                                           # Mais à frente iremos descobrir se contém subcategorias ou não
        
        # Enquanto a função check_subcategory retornar True, então ainda existem subcategorias.
        while check_subcategory(appended_category, final_category, categories_python_file):
            print("\nSubcategorias:")
            subcategories = []

            for category in categories_python_file:
                # Este if verifica se a final_category está na category e exclui caso seja igual à category em si (nesse caso não tem subcategoria)
                if final_category in category and final_category != category:
                    min_length = min(len(final_category), len(category)) # Verifica qual string tem menor tamanho
                    
                    a = 0
                    # Este ciclo for verifica se a final_category está no inicio da category.
                    # Se isto não fosse verificado, categorias como commercial.food_and_drink.ice_cream , catering.cafe.ice_cream , catering.ice_cream dariam conflito.
                    for char in range(min_length):
                        if final_category[char] == category[char]:
                            a += 1

                    # Esta lista é referente à divisão de uma categoria em subcategoria, por exemplo "a.b.c" fica ["a", "b", "c"] sendo que pouco a pouco se vai percorrendo
                    # a categoria de forma a ir substituindo "a." por "", depois "a.b." por "" até já não haver mais subcategorias
                    subcategory = list(category.replace(final_category+".","").split("."))[0]

                    # Se a categoria for válida (a == min_lenght) e já não estiver nas subcategories, então adicionamos à lista subcategories.
                    if a == min_length and subcategory not in subcategories:
                        subcategories.append(subcategory)

            # Apresenta todas as subcategories.
            for item in subcategories:
                print(f"\u2022 {item}")

            # Pede uma subcategoria ao utilizador.
            appended_category = input("\nSubcategoria:\n=> ").lower().strip()

            # Enquanto a subcategoria introduzida não estiver na lista de subcategorias, então ou é uma string vazia ou uma subcategoria inválida.
            while appended_category not in subcategories:
                if appended_category != "":
                    appended_category = input("\n\u26A0 Tem de escolher uma subcategoria válida! \u26A0\nSubcategoria:\n=> ")
                else:
                    break
            
            # Se a subcategoria não for uma string vazia, então, adicionamos à categoria final.
            if appended_category != "":
                final_category += "."+appended_category
        
        # Se a variável categories estiver vazia então damos-lhe o valor da primeira final_category a ser criada (com ou sem subcategorias)
        if categories == "":
            categories = final_category
        # Senão, aumentamos o número de categoria separando com uma vírgula.
        else:
            categories += ","+final_category
        
        # Enquanto a "appended_category" não for vazia, será pedido ao utilizador que adicione uma nova categoria. O ciclo acaba quando appended_category for igual a "".
        i += 1
        show_main_categories(categories_python_file)
        appended_category = input(f"\nCategoria {i}:\n=> ").strip().lower()

        # Enquanto a "appended_category" não for vazia, será pedido ao utilizador que adicione uma nova categoria. O ciclo acaba quando appended_category for igual a "".
        while appended_category not in categories_python_file:
            # Se appended_category não for uma string vazia, então é inválida
            if appended_category != "":
                appended_category = input(f"\n\u26A0 Tem de escolher uma categoria válida! \u26A0\nCategoria {i}:\n=> ").lower().strip()
            # Senão, significa que o utilizador quer terminar de adicionar categorias, logo o ciclo é quebrado.
            else:
                break
    
    return categories

# Esta função verifica se o "file_name" tem algum caracter inválido ou não. (Caracteres inválido: "\", "/", "|", "?", "<", ">", "*", ":", "“")
def has_valid_chars(file_name):
    for char in ("\\", "/", "|", "?", "<", ">", "*", ":", "“"):
        if char in file_name:
            return False
        
    return True

# Esta função exporta os dados recolhidos pela API para um ficheiro CSV.
def csv_export(total_attractions, formatted_data, average_distance):
    file_name = input("Insira um nome para o ficheiro: ")

    # Enquanto a função has_valid_chars não retornar True, então é porque o nome do ficheiro não é válido.
    while not has_valid_chars(file_name):
        file_name = input("\u26A0 Nome inválido! \u26A0\nO nome do ficheiro não pode incluir nenhum dos seguintes caracteres: \\, /, |, ?, <, >, *, :, “\nInsira um nome para o ficheiro: ")

    # Cria um ficheiro chamado {file_name}.csv caso ainda não tenha sido criado.
    with open(f"{file_name}.csv", "w", encoding="utf-8") as fileobj:
        writer = csv.writer(fileobj)
        # Adiciona a primeira linha do ficheiro CSV com os nomes dos dados que serão escritos nas linhas seguintes.
        writer.writerow(["Nome", "País", "Distrito", "Concelho", "Freguesia", "Latitude", "Longitude", "Distância"])

        # Este ciclo for itera pelas diferentes atrações e adiciona uma linha ordenada ao ficheiro CSV.
        for attraction in range(len(formatted_data)):
            property = formatted_data[attraction]
            # Adiciona uma linha ordenada com as propriedades da atração ao ficheiro CSV.
            writer.writerow([property["name"], property["country"], property["county"], property["city"], property["district"], property["lat"],property["lon"], property["distance"]])

        # Adiciona as estatísticas finais ao ficheiro CSV
        writer.writerow([f"\n--- Estatísticas ---\nTotal de Atrações: {total_attractions}\nDistância média das atrações: {average_distance/1000}km"])

    # Informa o utilizador de que o ficheiro foi criado com sucesso.
    print(f"O ficheiro {file_name}.csv foi criado na pasta do projeto.")

def store_and_format_data(data_dict):
    total_attractions = 0
    average_distance = 0
    formatted_data = [] # Uma lista que irá conter um dicionário por cada atração válida (que tenha nome)

    # A variável table é criada através de uma função de um módulo. Como parâmetros, introduzi o que queria que aparecesse na primeira linha/topo da tabela.
    table = PrettyTable(["Nome", "\u2690 País", "\U0001F3DB  Distrito", "\U0001F3E2 Concelho", "\U0001F3D8  Freguesia", "\U0001F79C  Localização (Lat,Lon)", "Distância (km)"])

    # Este ciclo for itera por todas as atrações devolvidas pela API (incluindo as inválidas que não têm nome)
    for i in range(len(data_dict["features"])):
        properties = data_dict["features"][i]["properties"]

        # Por defeito, todas as propriedades começam com o valor None.
        properties_dict = {"name": None, "country": None, "county": None, "city": None, "district": None, "lat": None, "lon": None, "distance": None}

        for item in ("name", "country", "county", "city", "district", "lat", "lon", "distance"):
            # Caso o item não esteja nas propriedades é definido como "Sem informação"
            if item not in properties:
                properties_dict[item] = "Sem informação"
            # Senão será dado o valor retribuido pela API.
            else:
                properties_dict[item] = properties[item]
            # Se já estivermos no último item ("distance") e o "name" estiver nas propriedades, então esta atração é válida
            # Logo, adicionamos as informações à lista formatted_data, contabilizamos como uma atração e também a sua distância.
            if item == "distance" and "name" in properties:
                formatted_data.append(properties_dict) # Adiciona um dicionário com a informação de uma atração
                total_attractions += 1
                average_distance += float(properties_dict["distance"])

    # Depois de organizar a informação toda, então o passo seguinte é formatar essa informação numa tabela adicionando uma linha com informações e uma linha vazia.
    for i in range(len(formatted_data)):
        property = formatted_data[i]
        table.add_row([property["name"], property["country"], property["county"], property["city"], property["district"], f'{property["lat"]},{property["lon"]}', property["distance"]/1000])
        table.add_row(["","","","","","",""])

    # Elimina a última linha da tabela de forma a que não fique uma linha vazia (uma vez que o ciclo for anterior adicionava uma linha vazia após cada elemento).
    table.del_row(len(table._rows)-1)

    # Caso o número total de atrações seja nulo, então alertamos o utilizador de que não foram encontradas atrações.
    if total_attractions == 0:
        print("\n\u26A0  Não foram encontradas atrações que cumpram os requisitos introduzidos. \u26A0")
        choice = input("Deseja fazer outra pesquisa? (s/n)\n=> ").strip().lower() # Como a variável choice anterior não irá mais ser usada, usámos o mesmo nome para definir este input
        if choice == "s":
            restart()
        else:
            exit()

    # Visto que durante o ciclo for fomos adicionando todas as distâncias, no fim temos de dividir pelo número de atrações.
    average_distance = average_distance/total_attractions

    # A variável statistics_table é criada através de uma função de um módulo. Como parâmetros, introduzi o que queria que aparecesse na primeira linha/topo da tabela.
    statistics_table = PrettyTable(["Estatísticas"])
    statistics_table.add_row([f"No total foram encontradas {total_attractions} atrações."])
    statistics_table.add_row([f"A média da distância dessas atrações é de {average_distance/1000}km"])
            
    return total_attractions, average_distance, formatted_data, table, statistics_table

# A função main está subdividida em outras funções de forma a não poluir o código principal do programa e também facilitar a deteção de bugs.
def main():
    print(welcome)

    # Este ciclo while serve para repetir o menu sempre que o utilizador utilizar os comandos "1" e "2".
    while True:
        # A função menu_options() dá return de true se a opção escolhida for "Planear viagem", daí a necessidade de dar break no ciclo while caso essa seja a opção escolhida.
        if menu_options():
            break # Quando a opção escolhida é "2" (Planear viagem), o ciclo é quebrado através da função break.

    lon, lat, radius = define_inputs()

    print(f"OUTPUT_TESTE: lon = {lon}, lat = {lat}, radius = {radius}") # REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER

    categories = define_categories(categories_python_file)

    print("OUTPUT_TESTE: categories = "+categories) # REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER

    #url = f"https://api.geoapify.com/v2/places?categories={categories}" + f"&bias=proximity:{lon},{lat}" + "&apiKey=041fa32a7f874d2594bd27b29a1a39fd" + f"&filter=circle:{lon},{lat},{radius*1000}"
    url = "https://api.geoapify.com/v2/places?categories=service&bias=proximity:-8.483349,40.786700&apiKey=041fa32a7f874d2594bd27b29a1a39fd&filter=circle:-8.483349,40.786700,1000"
    
    # A variável resp resulta da resposta da API conforme os dados introduzidos (categories, filter, lon, lat, radius, etc...)
    resp = requests.get(f"{url}")

    print(url)                                   # REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER
    print("resp.status_code:", resp.status_code) # REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER REMOVER

    # A variável data_dict resulta da transformação da string devolvida pela API em uma estrutura de dados do Python, neste caso, um dicionário.
    data_dict = json.loads(resp.text)

    total_attractions, average_distance, formatted_data, table, statistics_table = store_and_format_data(data_dict)

    print(table)
    print(statistics_table)

    choice = input("Deseja exportar dados sobre as atrações para CSV? (s/n)\n=> ").strip().lower()
    if choice == "s":
        csv_export(total_attractions, formatted_data, average_distance)

    choice = input("Deseja fazer outra pesquisa? (s/n)\n=> ").strip().lower() # Como a variável choice anterior não irá mais ser usada, usámos o mesmo nome para definir este input
    if choice == "s":
        restart()
    else:
        exit()
    
main()