import requests
import json
import csv
import time

#get a pokemon from pokeapi
def getPokemon(pokemonID: int) -> dict:
    requestURL = "https://pokeapi.co/api/v2/pokemon/" + str(pokemonID)
    response = requests.get(requestURL)

    #check http response
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
    formatted = {
                "id": pokemonData['id'],
                "Name": pokemonData['name'],
                "Weight": pokemonData['weight']/1000, #divide by 1000 to get Kg
                "Height": pokemonData['height']/10, #divide by 10 to get meters
                }

    #format depending on type 2
    if len(pokemonData['types']) == 1:
        formatted.update({
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": "None",
                    })
    else:
        formatted.update({
                    "Type 1": pokemonData['types'][0]['type']['name'],
                    "Type 2": pokemonData['types'][1]['type']['name'],
                    })
        #add stats
    formatted.update({
            "hp": pokemonData['stats'][0]['base_stat'],
            "attack": pokemonData['stats'][1]['base_stat'], 
            "defense": pokemonData['stats'][2]['base_stat'], 
            "special-attack": pokemonData['stats'][3]['base_stat'], 
            "special-defense": pokemonData['stats'][4]['base_stat'], 
            "speed": pokemonData['stats'][5]['base_stat']
    })

    formatted

    return formatted

#write the CSV file with a list of formatted pokemonData, named using the selected generation
def writeCSV(formattedPokemonDataList, generation):
    with open(f'pokemonGen{generation}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "Name", "Weight", "Height", "Type 1", "Type 2", "hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(formattedPokemonDataList)

#select a generation between 1 and 9, or all generations
pokemonGen = input("select generation (1 - 9 or All(highly discouraged)) \n")

if (pokemonGen == "All"):
    print(
        "are you sure you want to run for all 1025 pokemon? \n",
        "I would really not recommend running this as it will take more than 8 minutes due to pre-programmed delay as well as the delay in the API and other unexpected run time delays. \n",
        "This might also use quite a large amount of memory. \n",
        "NOTE: you might get blocked by pokeapi.co if running this too much! \n"
        )
    result = input("(y/N) \n")
    if result == "y":
        print("running for all 1025 pokemon...")
        pokemonGenRange = range(1, 1026)
    else:
        print("cancelled...")
        exit(0)
elif (pokemonGen == "test"):
    print("test run, pulling first 9 pokemon")
    pokemonGenRange = range(1, 10)
elif (pokemonGen < 1 or pokemonGen > 9 ): 
    print("generation out of bounds")
    exit(1)
else:
    #set a range value based off the selected generation
    match pokemonGen:
        case 1:
            pokemonGenRange = range(1, 152)
        case 2:
            pokemonGenRange = range(152, 252)
        case 3:
            pokemonGenRange = range(252, 387)
        case 4:
            pokemonGenRange = range(387, 494)
        case 5:
            pokemonGenRange = range(494, 650)
        case 6:
            pokemonGenRange = range(650, 722)
        case 7:
            pokemonGenRange = range(722, 810)
        case 8:
            pokemonGenRange = range(810, 906)
        case 9:
            pokemonGenRange = range(906, 1026)

#list for data to be written to
formattedPokemonDataList = []
for i in pokemonGenRange:
    print("fetching:" + str(i) + " of " + str(pokemonGenRange.stop))
    data = getPokemon(i)
    formattedPokemonData = formatPokeData(data)
    formattedPokemonDataList.append(formattedPokemonData)
    time.sleep(0.5)

#output as .csv file
writeCSV(formattedPokemonDataList, pokemonGen)
print("finished")