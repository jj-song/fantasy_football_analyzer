import configparser
import json

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
data_path = config['path']['data']

oline_positions = ['LT', 'LG', 'C', 'RG', 'RT']

def get_team_oline(team):
    """
    This function returns all players in a team's offensive line.
    """
    file = open(data_path + team + '.json')
    data = json.load(file)
    player_data = dict()
    o_line_players = []

    for item in data:
        full_name = f"{item.get('firstName', '')} {item.get('lastName', '')}"
        position = item.get('position', "")
        overall_rating = item.get('overall_rating', "")
        if position in oline_positions:
            player_data['position'] = position
            player_data['overall_rating'] = overall_rating
            player_data['name'] = full_name
            player_data_copy = player_data.copy()
            o_line_players.append(player_data_copy)

    return o_line_players


def get_best_team_oline(team):
    """
    This function returns all players in a team's offensive line.
    """
    o_line_players = get_team_oline(team)
    top_players = dict()

    for player in o_line_players:
        # TODO: implement function is_injured here to determine current status of oline.
        if player['position'] in top_players:
            if player['overall_rating'] > top_players[player['position']]['overall_rating']:
                top_players[player['position']] = player
        else:
            top_players[player['position']] = player

    total = 0
    for i in oline_positions:
        total += top_players[i]['overall_rating']

    top_players['average'] = total/5

    return top_players