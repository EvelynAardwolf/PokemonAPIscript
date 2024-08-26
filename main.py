import requests

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
        
        print(pokemonData)
        return 
    else:
        print("request returned: " + response.status_code)
        return None



print(getPokemon(input("Enter pokemon ID \n")))