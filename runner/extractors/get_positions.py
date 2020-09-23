import configparser
import json

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
data_path = config['path']['data']

def position_has_two_slots(position):
    return any(char.isdigit() for char in position)

def get_players(team, positions):
    """
    This function returns all players given positions
    """
    file = open(data_path + team + '.json')
    data = json.load(file)
    player_data = dict()
    position_players = []

    for item in data:
        full_name = f"{item.get('firstName', '')} {item.get('lastName', '')}"
        position = item.get('position', "")
        overall_rating = item.get('overall_rating', "")

        if position in positions.keys():
            player_data['position'] = position
            player_data['overall_rating'] = overall_rating
            player_data['name'] = full_name
            player_data_copy = player_data.copy()
            position_players.append(player_data_copy)

    return position_players


def get_best_players(team, positions):
    """
    This function returns all the best players given positions
    """
    all_players_of_position = get_players(team, positions)
    top_players = dict()

    for player in all_players_of_position:
        # TODO: implement function is_injured here to determine current status of oline.
        position = player['position']
        if positions[position] > 1:
            # TODO: change this so that it can handle dynamically, even for positions when it's has more than 2 slots.
            #       Right now, it handles only up to 2 slots because it is hardcoded.
            if player['position']+'1' in top_players:
                if player['overall_rating'] > top_players[player['position']+'1']['overall_rating']:
                    top_players[player['position']+'2'] = top_players[player['position'] + '1']
                    top_players[player['position'] + '1'] = player
                else:
                    if player['position']+'2' in top_players:
                        if player['overall_rating'] > top_players[player['position']+'2']['overall_rating']:
                            top_players[player['position'] + '2'] = player
                    else:
                        top_players[player['position']+'2'] = player
            else:
                top_players[player['position']+'1'] = player
        else:
            # This is for 99% of the cases, where the position being iterated has a dictionary value of 1.
            if player['position'] in top_players:
                if player['overall_rating'] > top_players[player['position']]['overall_rating']:
                    top_players[player['position']] = player
            else:
                top_players[player['position']] = player

    total = 0
    for i in top_players.keys():
        total += top_players[i]['overall_rating']

    top_players['average'] = total/len(top_players.keys())

    return top_players