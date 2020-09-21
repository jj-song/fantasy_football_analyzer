import configparser
import json

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
data_path = config['path']['data']

def get_high_awareness_49ers():
    """
    This function serves as a placeholder for future unit tests.
    This function proves data is in good condition and basically functionality
    of the script works.
    """
    file = open(data_path + '49ers.json')
    data = json.load(file)
    high_awareness_players = []

    for item in data:
        full_name = f"{item.get('firstName', '')} {item.get('lastName', '')}"
        awareness_rating = item.get('awareness_rating', 0)
        if awareness_rating > 80:
            high_awareness_players.append(full_name)

    return high_awareness_players
