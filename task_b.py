# there are 18 pokemon types not considering stellar as a separate type

import requests
import pandas as pd # to use a dataframe to make the matrix
import json

session = requests.session()

type_url = "https://pokeapi.co/api/v2/type/"

def get_dmg_dict():
    dmg_dict = {}
    for i in range(1, 19):
        data = session.get(type_url + str(i)).json()
        dmg_data = data['damage_relations']
        typename = data['name']
        
        d = {}

        for j in dmg_data['half_damage_to']:
            d[j['name']] = 0.5

        for j in dmg_data['double_damage_to']:
            d[j['name']] = 2

        for j in dmg_data['no_damage_to']:
            d[j['name']] = 0

        dmg_dict[typename] = d
    
    return dmg_dict

def gen_json():
    # call this function to generate a json file of the type matchups

    dmg_dict = get_dmg_dict()

    with open("poketypes.json", "w") as f:
        json.dump(dmg_dict, f, indent = 2)


# uncomment the line below to generate the json file necessary for api.py it takes some time so its commented
# gen_json()

# generating json to not have to call the api multiple times

with open("poketypes.json") as f:
    dmg_dict = json.load(f)

dmg_matrix = pd.DataFrame(dmg_dict)

# to replace NaN with 1 in the matrix

filled_dmg_matrix = dmg_matrix.fillna(1)

# the columns are the attacking types , rows are the defending types
# so syntax would be like filled_dmg_matrix[attacker][defender]
print(filled_dmg_matrix) 

# full matrix is not visible in the terminal , to convert to csv
filled_dmg_matrix.to_csv("poketypes.csv")