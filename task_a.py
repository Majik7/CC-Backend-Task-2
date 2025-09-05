import requests
import json # for json formatting
import sys

base_url = "https://pokeapi.co/api/v2/"

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
	filename = "pokemon_output"

def get_name(jsonfile):
    return jsonfile['name']

def get_ability(jsonfile):
    l = []
    for i in jsonfile['abilities']:
        l += [i['ability']['name']]

    return l

def get_id(jsonfile):
    return jsonfile['id']

def get_types(jsonfile):
    l = []
    for i in jsonfile['types']:
        l += [i['type']['name']]

    return l

with open("pokemon.txt") as f:
    s = f.readlines()
    pokelist = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, s)) # adjusting the map for magikarp else it was cut to magikar due to no \n
    # print(pokelist)

pokedata = {}

session = requests.session() # to avoid multiple calls

for i in pokelist:
        url_1 = base_url + f"pokemon/{i}"
        url_2 = base_url + f"pokemon-species/{i}"
        res_1 = session.get(url_1) # for everything else
        res_2 = session.get(url_2) # for legendary and mythical

        if res_1.status_code == 200 and res_2.status_code == 200:
            data_1 = res_1.json()
            data_2 = res_2.json()
            d = {}

            d['id'] = get_id(data_1)
            d['abilities'] = get_ability(data_1)
            d['types'] = get_types(data_1)
            d['is_legendary'] = data_2['is_legendary']
            d['is_mythical'] = data_2['is_mythical']

            pokedata[data_1['name']] = d

        else:
             print(f"error on pokemon {i}")

with open(f"{filename}.json", "w") as f:
        json.dump(pokedata, f, indent = 2)