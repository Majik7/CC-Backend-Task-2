from flask import Flask, request
import json
import pandas as pd
import requests
import sys

app = Flask(__name__)

try:
    with open("poketypes.json") as f:
        pokejson = json.load(f)

except FileNotFoundError:
    print("The json file doesn't exist yet , please run task_b.py")
    sys.exit()

pokedf = pd.DataFrame(pokejson).fillna(1)

@app.route('/')
def home():
    return {"message": "Use /api"}

@app.route('/api')
def typematchup():
    atype = request.args.get("attacker")
    dtype = request.args.get("defender")

    if atype:
        atype = atype.lower()

    if dtype:
        dtype = dtype.lower()

    if not atype and not dtype:
        return {"message": "url syntax is /api?attacker={attacktype}&defender={defendtype} or /api/pokemon/{pokemon_name_or_id}"}

    elif atype and dtype:
        return {"attacker": atype, "defender": dtype, "multiplier": pokedf[atype][dtype]}
    
    elif not dtype:
        d = {}

        for i in pokedf.index:
            d[i] = pokedf[atype][i]

        return {"attacker": atype, "to_defenders": d}
    
    elif not atype:
        d = {}
        
        for i in pokedf.columns:
            d[i] = pokedf[i][dtype]

        return {"defender": dtype, "from_attackers": d}

@app.route('/api/pokemon/<x>')
def inputpokemon(x):
    url = "https://pokeapi.co/api/v2/pokemon/" + str(x)
    data = requests.get(url).json()

    typelist = []

    for i in data['types']:
        typelist += [i['type']['name']]

    if len(typelist) == 1:
        doubleweak = []
        immunity = []

        for i in pokedf.columns:
            if pokedf[i][typelist[0]] == 2:
                doubleweak += [i]
            
            elif pokedf[i][typelist[0]] == 0:
                immunity += [i]

        return {"pokemon": data['name'], "type": typelist, "twice_weak_to": doubleweak, "immune_to": immunity}
    
    elif len(typelist) == 2:
        doubleweak = []
        fourweak = []
        immunity = []

        for i in pokedf.columns:
            if pokedf[i][typelist[0]] * pokedf[i][typelist[1]] == 0:
                immunity += [i]
            
            elif pokedf[i][typelist[0]] * pokedf[i][typelist[1]] == 2:
                doubleweak += [i]

            elif pokedf[i][typelist[0]] * pokedf[i][typelist[1]] == 4:
                fourweak += [i]

        return {"pokemon": data['name'], "type": typelist, "twice_weak_to": doubleweak, "quadruple_weak_to": fourweak, "immune_to": immunity}

if __name__ == '__main__':
    app.run(host = "localhost", port = 8000)