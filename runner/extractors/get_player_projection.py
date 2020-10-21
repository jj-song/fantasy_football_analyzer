import configparser
import json
from runner.utilities.constants import d_front_7_positions,d_secondary_positions,o_line_positions,o_skilled_positions
from runner.extractors.get_positions import get_best_players_of_team
from runner.utilities.mapping import fullTeam_shortTeam_map

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))
players_path = config['path']['players']
injuries_path = config['path']['injuries']
schedule_path = config['path']['schedule']
data_file_type = config['constants']['data_file_type']

def get_player_accessory_data(team, player, week):
    """
    This function returns all players given positions
    """
    madden_file = open(players_path + team + data_file_type)
    madden_data = json.load(madden_file)
    overall_data = dict()
    player_data = dict()
    player_value = 0

    for madden_datum in madden_data:
        full_name = f"{madden_datum.get('firstName', '')} {madden_datum.get('lastName', '')}"
        position = madden_datum.get('position', "")

        if full_name == player:
            # Function to get which team he's up against
            if team == 'Football_Team':
                opposing_team = get_opposing_team('Football Team', week)
            else:
                opposing_team = get_opposing_team(team, week)
            if opposing_team is not None:
                opposing_team_mapped = fullTeam_shortTeam_map[opposing_team]
                if position == 'HB':
                    overall_data = get_weighted_rb_value(full_name, madden_datum, team, opposing_team_mapped)
                elif position == 'WR':
                    overall_data = get_weighted_wr_value(full_name, madden_datum, team, opposing_team_mapped)
                elif position == 'QB':
                    overall_data = get_weighted_qb_value(full_name, madden_datum, team, opposing_team_mapped)

            return overall_data

    if not overall_data:
        overall_data['name'] = player
        overall_data['position'] = "bye"
        overall_data['player_madden_rating'] = 0
        overall_data['player_o_line_avg'] = 0
        overall_data['opponent_d_front_7_avg'] = 0
        overall_data['opponent_d_secondary_avg'] = 0


def get_opposing_team(player_team, week):

    schedule_file = open(schedule_path + 'schedule' + data_file_type)
    schedule_data = json.load(schedule_file)

    for game in schedule_data:
        if game.get('Week') == str(week):
            if game.get('Winner/tie', '').find(player_team) != -1:
                opponent_team = game.get('Loser/tie', '')
                return opponent_team
            elif game.get('Loser/tie', '').find(player_team) != -1:
                opponent_team = game.get('Winner/tie', '')
                return opponent_team

def get_weighted_rb_value(full_name, madden_datum, player_team, opposing_team):
    overall_data = dict()
    overall_data['name'] = full_name
    overall_data['position'] = madden_datum.get('position')
    overall_data['player_madden_rating'] = madden_datum.get('overall_rating')
    overall_data['player_o_line_avg'] = get_best_players_of_team(player_team, o_line_positions).get('average')
    overall_data['opponent_d_front_7_avg'] = get_best_players_of_team(opposing_team, d_front_7_positions).get('average')
    overall_data['opponent_d_secondary_avg'] = get_best_players_of_team(opposing_team, d_secondary_positions).get('average')
    # TODO: Do some more research to update the formula here. This is the most important part of the program since it will give you the actual
    #       Weighted values of the players
    overall_data['weighted_player_rating'] = overall_data['player_madden_rating'] + (overall_data['player_o_line_avg'] - overall_data['opponent_d_front_7_avg'])

    return overall_data

def get_weighted_wr_value(full_name, madden_datum, player_team, opposing_team):
    overall_data = dict()
    overall_data['name'] = full_name
    overall_data['position'] = madden_datum.get('position')
    overall_data['player_madden_rating'] = madden_datum.get('overall_rating')
    overall_data['player_o_line_avg'] = get_best_players_of_team(player_team, o_line_positions).get('average')
    overall_data['opponent_d_front_7_avg'] = get_best_players_of_team(opposing_team, d_front_7_positions).get('average')
    overall_data['opponent_d_secondary_avg'] = get_best_players_of_team(opposing_team, d_secondary_positions).get('average')
    overall_data['player_qb'] = get_best_players_of_team(player_team, o_skilled_positions).get('QB').get('overall_rating')
    # TODO: Do some more research to update the formula here. This is the most important part of the program since it will give you the actual
    #       Weighted values of the players
    overall_data['weighted_player_rating'] = overall_data['player_madden_rating'] + \
                                             (
                                                (overall_data['player_o_line_avg']*.75 + overall_data['player_qb']*.25)
                                              - (overall_data['opponent_d_front_7_avg']*.50 + overall_data['opponent_d_secondary_avg']*.50)
                                              )
    if not overall_data['weighted_player_rating']:
        overall_data['weighted_player_rating'] = 0
    return overall_data

def get_weighted_qb_value(full_name, madden_datum, player_team, opposing_team):
    overall_data = dict()
    overall_data['name'] = full_name
    overall_data['position'] = madden_datum.get('position')
    overall_data['player_madden_rating'] = madden_datum.get('overall_rating')
    overall_data['player_o_line_avg'] = get_best_players_of_team(player_team, o_line_positions).get('average')
    overall_data['opponent_d_front_7_avg'] = get_best_players_of_team(opposing_team, d_front_7_positions).get(
        'average')
    overall_data['opponent_d_secondary_avg'] = get_best_players_of_team(opposing_team, d_secondary_positions).get(
        'average')
    wr1 = get_best_players_of_team(player_team, o_skilled_positions).get('WR1')
    wr2 = get_best_players_of_team(player_team, o_skilled_positions).get('WR2')

    # TODO: Do some more research to update the formula here. This is the most important part of the program since it will give you the actual
    #       Weighted values of the players

    overall_data['weighted_wr1_rating'] = get_weighted_wr_value(wr1.get('name'), wr1, player_team, opposing_team).get('weighted_player_rating')
    overall_data['weighted_wr2_rating'] = get_weighted_wr_value(wr2.get('name'), wr2, player_team, opposing_team).get('weighted_player_rating')

    overall_data['weighted_player_rating'] = overall_data['player_madden_rating'] + (overall_data['player_o_line_avg'] - overall_data['opponent_d_front_7_avg']) \
                                             + ((overall_data['weighted_wr1_rating'] * .6 +  overall_data['weighted_wr2_rating'] * .4) -
                                                (overall_data['opponent_d_secondary_avg']))
    if full_name == 'C.J. Beathard':
        print("hi")
    if not overall_data['weighted_player_rating']:
        overall_data['weighted_player_rating'] = 0
    return overall_data
