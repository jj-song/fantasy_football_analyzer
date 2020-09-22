import configparser
import json

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
data_path = config['path']['data']

def is_injured(player):
    """
    This function will return injury status of a player
    """
    injured = False

    return injured
