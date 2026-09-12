import httpx


def get_pokemon_from_pokeapi(name_or_id: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{name_or_id.lower()}"

    response = httpx.get(url)

    if response.status_code == 404:
        return None

    response.raise_for_status()

    pokemon = response.json()

    return {
        "id": pokemon["id"],
        "name": pokemon["name"],
        "types": [
            type_info["type"]["name"]
            for type_info in pokemon["types"]
        ],
        "abilities": [
            ability_info["ability"]["name"]
            for ability_info in pokemon["abilities"]
        ],
        "sprite": pokemon["sprites"]["front_default"]
    }
    
def get_pokemon_moves_from_pokeapi(name_or_id: str):
    value = str(name_or_id).lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{value}"
    response = httpx.get(url, timeout=30)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    pokemon = response.json()
    moves = [
        move_info["move"]["name"]
        for move_info in pokemon["moves"]
    ]
    return {
        "pokemon_id": pokemon["id"],
        "pokemon_name": pokemon["name"],
        "moves": moves
    }
