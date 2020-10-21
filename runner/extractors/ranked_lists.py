import configparser
from runner.utilities.constants import d_front_7_positions,d_secondary_positions,o_line_positions,o_skilled_positions, fantasy_positions
from runner.utilities.data_sorter import list_sort_by_dict_value
from runner.extractors.get_positions import get_best_players_of_team, get_all_players_on_team
from runner.extractors.get_player_projection import get_player_accessory_data

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
players_path = config['path']['players']
injuries_path = config['path']['injuries']
data_file_type = config['constants']['data_file_type']
injury_designations = ['doubtful', 'out', 'I-R']


def get_ranked_team_group_positions():
    """
    This function returns a sorted list of team overall ratings for various groups of positions
    """
    team_d_front_7 = dict()
    team_d_secondary = dict()
    team_o_line = dict()
    team_o_skilled = dict()


    for team in teams:
        team_d_front_7[team] = get_best_players_of_team(team, d_front_7_positions)
        team_d_secondary[team] = get_best_players_of_team(team, d_secondary_positions)
        team_o_line[team] = get_best_players_of_team(team, o_line_positions)
        team_o_skilled[team] = get_best_players_of_team(team, o_skilled_positions)

    top_d_front_7_avg = list_sort_by_dict_value(team_d_front_7, 'average')
    top_d_secondary_avg = list_sort_by_dict_value(team_d_secondary, 'average')
    top_o_line_avg = list_sort_by_dict_value(team_o_line, 'average')
    top_o_skilled_avg = list_sort_by_dict_value(team_o_skilled, 'average')

    return top_d_front_7_avg, top_d_secondary_avg, top_o_line_avg, top_o_skilled_avg

def get_ranked_positions():
    """
    This function returns a sorted list of team overall ratings for various groups of positions
    """
    team_all = dict()
    players_weighted_qb = dict()
    players_weighted_wr = dict()
    players_weighted_rb = dict()
    for team in teams:
        team_all[team] = get_all_players_on_team(team, fantasy_positions)
        for player in team_all[team]:
            name = player.get('name')
            position = player.get('position')
            # if name == 'Drew Brees':
            #     print("hi")
            if position == 'QB':
                players_weighted_qb[name] = get_player_accessory_data(team=team, player=name, week=7)
            elif position == 'WR':
                players_weighted_wr[name] = get_player_accessory_data(team=team, player=name, week=7)
            elif position == 'HB':
                players_weighted_rb[name] = get_player_accessory_data(team=team, player=name, week=7)

    for x in list(players_weighted_qb.keys()):
        if len(players_weighted_qb[x]) == 0:
            del players_weighted_qb[x]

    for x in list(players_weighted_wr.keys()):
        if len(players_weighted_wr[x]) == 0:
            del players_weighted_wr[x]

    for x in list(players_weighted_rb.keys()):
        if len(players_weighted_rb[x]) == 0:
            del players_weighted_rb[x]

    top_qb = list_sort_by_dict_value(players_weighted_qb, 'weighted_player_rating')
    top_wr = list_sort_by_dict_value(players_weighted_wr, 'weighted_player_rating')
    top_rb = list_sort_by_dict_value(players_weighted_rb, 'weighted_player_rating')

    return top_qb, top_wr, top_rb