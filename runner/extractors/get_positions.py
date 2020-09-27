import configparser
import json
from runner.utilities.mapping import fullTeam_shortCity_map

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
players_path = config['path']['players']
injuries_path = config['path']['injuries']
data_file_type = config['constants']['data_file_type']
injury_designations = ['doubtful', 'out', 'I-R']


def get_all_players_on_team(team, positions):
    """
    This function returns all players given positions
    """
    madden_file = open(players_path + team + data_file_type)
    madden_data = json.load(madden_file)

    injury_file = open(injuries_path+'injuries'+data_file_type)
    injury_data = json.load(injury_file)

    player_data = dict()
    position_players = []

    for player in madden_data:
        full_name = f"{player.get('firstName', '')} {player.get('lastName', '')}"
        position = player.get('position', "")
        overall_rating = player.get('overall_rating', "")

        if position in positions.keys():
            player_data['position'] = position
            player_data['overall_rating'] = overall_rating
            player_data['name'] = full_name
            player_data_copy = player_data.copy()
            position_players.append(player_data_copy)

    # aggregated a list of injured players on that team.
    team_injuries = []
    for injured_player in injury_data:
        if injured_player['Tm'] == fullTeam_shortCity_map[team]:
            team_injuries.append(injured_player)

    # compared injured player list with player list to remove injured players from final list.
    position_players_to_return = position_players.copy()
    for position_player in position_players:
        for team_injury in team_injuries:
            if position_player['name'] == team_injury['Player'] and \
                    team_injury['Class'] in injury_designations:
                position_players_to_return.remove(position_player)

    return position_players_to_return


def get_best_players_of_team(team, positions):
    """
    This function returns all the best players given positions
    """
    all_players_of_position = get_all_players_on_team(team, positions)
    top_players = dict()

    for player in all_players_of_position:
        position = player['position']
        num_of_positions = positions[position]
        if num_of_positions > 1:
            # TODO: change this so that it can handle dynamically, even for positions when it's has more than 2 slots.
            #       Right now, it handles only up to 2 slots because it is hardcoded.
            #       Added a bit more to it but it still breaks when num_position is > 2.
            for i in range(1, num_of_positions):
                if player['position'] + str(i) in top_players:
                    if player['overall_rating'] > top_players[player['position'] + str(i)]['overall_rating']:
                        top_players[player['position'] + str(i+1)] = top_players[player['position'] + str(i)]
                        top_players[player['position'] + str(i)] = player
                    else:
                        if player['position'] + str(i+1) in top_players:
                            if player['overall_rating'] > top_players[player['position'] + str(i+1)]['overall_rating']:
                                top_players[player['position'] + str(i+1)] = player
                        else:
                            top_players[player['position'] + str(i+1)] = player
                else:
                    top_players[player['position'] + str(i)] = player
        else:
            # This is for 99% of the cases, where the position being iterated has a dictionary value of 1.
            if player['position'] in top_players:
                if player['overall_rating'] > top_players[player['position']]['overall_rating']:
                    top_players[player['position']] = player
            else:
                top_players[player['position']] = player

    #TODO: Right now, if all the available players who play a require position is injured, it removes that position entirely.
    #      This is just a bandaid. It removes it to make sure the average isn't tremendously off. But it should be made so that
    #      If lets say all the RG (right guard) were injured for Redskins, you should be able to bring the next highest rated
    #      o_line position player that wasn't previously being utilized. This likely more or less reflects what happens in
    #      real life.
    total = 0
    for i in top_players.keys():
        total += top_players[i]['overall_rating']

    top_players['average'] = total/len(top_players.keys())

    return top_players