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
def formatPokeData(pokemonData):
    #print(len(pokemonData['types']))
    if len(pokemonData['types']) == 1:
        print(f"id: {pokemonData['id']}",
            f"Name: {pokemonData['name']}",
            f"Weight: {pokemonData['weight']/1000} kg",
            f"Height: {pokemonData['height']/10} m",
            f"type 1: {pokemonData['types'][0]['type']['name']}",
            f"type 2: none", 
            f"base stats: ",
            f"  hp: {pokemonData['stats'][0]['base_stat']}",
            f"  attack: {pokemonData['stats'][1]['base_stat']}",
            f"  defense: {pokemonData['stats'][2]['base_stat']}",
            f"  special-attack: {pokemonData['stats'][3]['base_stat']}",
            f"  special-defence: {pokemonData['stats'][4]['base_stat']}",
            f"  speed: {pokemonData['stats'][5]['base_stat']}",
            sep="\n"
            )
    else:
        print(f"id: {pokemonData['id']}",
            f"Name: {pokemonData['name']}",
            f"Weight: {pokemonData['weight']/1000} kg",
            f"Height: {pokemonData['height']/10} m",
            f"type 1: {pokemonData['types'][0]['type']['name']}",
            f"type 2: {pokemonData['types'][1]['type']['name']}", 
            f"base stats: ",
            f"  hp: {pokemonData['stats'][0]['base_stat']}",
            f"  attack: {pokemonData['stats'][1]['base_stat']}",
            f"  defense: {pokemonData['stats'][2]['base_stat']}",
            f"  special-attack: {pokemonData['stats'][3]['base_stat']}",
            f"  special-defence: {pokemonData['stats'][4]['base_stat']}",
            f"  speed: {pokemonData['stats'][5]['base_stat']}",
            sep="\n"
            )
    return


def writeCSV(formattedPokemonDataList, generation):
    with open(f'pokemonGen{generation}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Number", "Name", "Weight", "Height", "Type 1" "Type 2", "Stats"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(formattedPokemonDataList)


#pokemongen = input("select generation \n")



data = getPokemon(input("Enter pokemon ID \n"))
formatPokeData(data)