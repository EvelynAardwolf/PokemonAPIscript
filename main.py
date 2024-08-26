import requests
import json
import csv

#function to get a pokemon from pokeapi
def getPokemon(pokemonID: int) -> dict:
    requestURL = "https://pokeapi.co/api/v2/pokemon/" + str(pokemonID)
    response = requests.get(requestURL)

    if response.status_code == 200:
        data = response.json()
        #print(data)
        pokemonData = {
        "id": data.pop("id"),
        "name": data.pop("name"),
        "weight": data.pop("weight"),
        "height": data.pop("height"),
        "stats": data.pop("stats"),
        "types": data.pop("types")
        }
        del(data)
        #print(pokemonData)
        return pokemonData
    else:
        print("request returned: " + response.status_code)
        exit(1)
    

#format the pokemon data into a readable string
def formatPokeData(pokemonData) -> dict:
    #print(len(pokemonData['types']))
    basestats = {
                "hp": pokemonData['stats'][0]['base_stat'],
                "attack": pokemonData['stats'][1]['base_stat'], 
                "defense": pokemonData['stats'][2]['base_stat'], 
                "special-attack": pokemonData['stats'][3]['base_stat'], 
                "special-defence": pokemonData['stats'][4]['base_stat'], 
                "speed": pokemonData['stats'][5]['base_stat']
                }


    if len(pokemonData['types']) == 1:
        formatted = {
                    "id": pokemonData['id'],
                    "Name": pokemonData['name'],
                    "Weight": pokemonData['weight']/1000,
                    "Height": pokemonData['height']/10,
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": "None",
                    "Stats": basestats
                    }
    else:
        formatted = {
                    "id": pokemonData['id'],
                    "Name": pokemonData['name'],
                    "Weight": pokemonData['weight']/1000,
                    "Height": pokemonData['height']/10,
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": pokemonData['types'][1]['type']['name'],
                    "Stats": basestats
                    }

    return formatted


def writeCSV(formattedPokemonDataList, generation):
    with open(f'pokemonGen{generation}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "Name", "Weight", "Height", "Type 1" "Type 2", "Stats"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(formattedPokemonDataList)

pokemonGen = input("select generation \n")
pokemonGenRange = range(1, pokemonGen)

formattedPokemonDataList = []
for i in pokemonGenRange:
    data = getPokemon(i)
    formattedPokemonData = formatPokeData(data)
    formattedPokemonDataList.append(formattedPokemonData)


writeCSV(formattedPokemonDataList, pokemonGen)