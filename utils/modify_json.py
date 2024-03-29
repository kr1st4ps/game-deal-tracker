def update(console, names_json, full_json):
    #   Collects games from the local json
    games_in_full_json = []
    for game in full_json:
        games_in_full_json.append(game["name"])

    #   Adds new games (if any) to local json
    for game in names_json:
        if game in games_in_full_json:
            games_in_full_json.remove(game)
        else:
            full_json = add(game, full_json, console)

    #   Removes (if needed) games from local json
    for game in games_in_full_json:
        full_json = remove(game, full_json)
    
    return full_json

def remove(name, games):
    for i in range(len(games)):
        if games[i]["name"] == name:
            games.pop(i)
            break

    return games

def add(name, games, console):

    new_data = {
        "name": name,
        "price": None,
        "best price": None,
        "full price": None,
        "ps plus": None
    }
    
    games.append(new_data)

    return games