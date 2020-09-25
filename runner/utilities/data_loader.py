import pandas as pd
from requests import get
import configparser
import requests
import json
from bs4 import BeautifulSoup
from sys import argv

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
data_path = config['path']['data']
injuries_path = config['path']['injuries']
schedule_path = config['path']['schedule']
data_file_type = config['constants']['data_file_type']

madden_ratings_api = config['madden']['api_url']
madden_filter = config['madden']['filter']

def load_madden_rating_data():
    """
    This function gathers player data using the madden rating API.
    The player data is saved under their respective team json files.
    """
    for team in teams:
        # TODO: When the Washington Football Team decides to actually claim a real name, you will need to change this.
        #       The logic below in lines 21 and 26 exist because Football Team is the only team which contain two words
        #       in the team name.
        madden_url = madden_ratings_api + madden_filter
        url = madden_url+team if team != 'Football Team' else 'https://ratings-api.ea.com/v2/entities/madden-nfl-21?limit=5000&filter=team:"Football Team"'
        output_file = data_path+team+data_file_type if team != 'Football Team' else 'C:/Users/Jihoon/Documents/Projects/fantasy_football_analyzer/data/Redskins.json'

        data_as_json = requests.get(url).json()
        df = pd.DataFrame(data_as_json['docs'])
        df.to_json(output_file, orient='records')


def load_injury_data():
    url = "https://www.pro-football-reference.com/players/injuries.htm"

    defColumnSettings = {
        'axis': 1,
        'inplace': True
    }

    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'injuries'})
    df = pd.read_html(str(table))[0]
    df.drop(['Details'],
            **defColumnSettings)

    df = df[df['Pos'] != 'Pos']

    df.fillna(0, inplace=True)

    output_file = injuries_path+'injuries'+data_file_type

    df.to_json(output_file, orient='records')


def load_schedule_data():
    url = "https://www.pro-football-reference.com/years/2020/games.htm"

    defColumnSettings = {
        'axis': 1,
        'inplace': True
    }

    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'games'})
    df = pd.read_html(str(table))[0]
    df.drop(['PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL', 'Unnamed: 5', 'Unnamed: 7'],
            **defColumnSettings)

    df = df[df['Week'] != 'Week']

    df.fillna(0, inplace=True)

    output_file = schedule_path+'schedule'+data_file_type

    df.to_json(output_file, orient='records')