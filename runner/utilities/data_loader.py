import pandas as pd
import requests
import configparser

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
data_path = config['path']['data']
data_file_type = config['constants']['data_file_type']
madden_ratings_api = config['madden']['api_url']
madden_filter = config['madden']['filter']

def load_data():
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