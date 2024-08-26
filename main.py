import requests
import json
import csv
import time

#get a pokemon from pokeapi
def getPokemon(pokemonID: int) -> dict:
    requestURL = "https://pokeapi.co/api/v2/pokemon/" + str(pokemonID)
    response = requests.get(requestURL)

    if response.status_code == 200:
        data = response.json()

        #filter  to only required data
        pokemonData = {
        "id": data.pop("id"),
        "name": data.pop("name"),
        "weight": data.pop("weight"),
        "height": data.pop("height"),
        "stats": data.pop("stats"),
        "types": data.pop("types")
        }

        del(data) #remove unused data to reduce memory load
        return pokemonData
    else:
        #exit on failed request to avoid errors in the file
        print("request returned: " + response.status_code)
        exit(response.status_code)
    

#format the pokemon data into a dict format for .csv
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
                    "Weight": pokemonData['weight']/1000, #divide by 1000 to get Kg
                    "Height": pokemonData['height']/10, #divide by 10 to get meters
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": "None",
                    "Stats": basestats
                    }
    else:
        formatted = {
                    "id": pokemonData['id'],
                    "Name": pokemonData['name'],
                    "Weight": pokemonData['weight']/1000, #divide by 1000 to get Kg
                    "Height": pokemonData['height']/10, #divide by 10 to get meters
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": pokemonData['types'][1]['type']['name'],
                    "Stats": basestats
                    }

    return formatted

#write the CSV file with a list of formatted pokemonData, named using the selected generation
def writeCSV(formattedPokemonDataList, generation):
    with open(f'pokemonGen{generation}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "Name", "Weight", "Height", "Type 1" "Type 2", "Stats"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(formattedPokemonDataList)





pokemonGen = int(input("select generation \n"))

pokemonGenRange = range(1, pokemonGen)

formattedPokemonDataList = []
for i in pokemonGenRange:
    data = getPokemon(i)
    formattedPokemonData = formatPokeData(data)
    formattedPokemonDataList.append(formattedPokemonData)
    time.sleep(0.3)

writeCSV(formattedPokemonDataList, pokemonGen)