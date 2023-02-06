def remove(name, games):
    for i in range(len(games)):
        if games[i]["name"] == name:
            games.pop(i)

    return games

def add(name, games, console):
    if console == "PS4":
        new_data = {
            "name": name,
            "price": None,
            "price plus": None,
            "best price": None,
            "base price": None
        }
    else:
        new_data = {
            "name": name,
            "price": None,
            "best price": None,
            "base price": None,
        }
    games.append(new_data)

    return games