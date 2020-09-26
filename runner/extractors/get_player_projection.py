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

    for madden_datum in madden_data:
        full_name = f"{madden_datum.get('firstName', '')} {madden_datum.get('lastName', '')}"
        position = madden_datum.get('position', "")
        player_rating = madden_datum.get('overall_rating', "")
        full_info = madden_datum

        if full_name == player:
            player_data['position'] = position
            player_data['player_rating'] = player_rating
            player_data['name'] = full_name
            overall_data['player_data'] = player_data

            # TODO: Function to get which team he's up against
            opposing_team = get_opposing_team(team, week)
            opposing_team_mapped = fullTeam_shortTeam_map[opposing_team]

            # TODO: Function to get rating for his oline:
            #       Depending on the position of player selected, it will lead querying for different items.
            #       For example, if it's a running back, put heavy weight on oline, and a little weight on
            #       QB and WR because otherwise they'll stack the box.
            overall_data['player_o_line_avg'] = get_best_players_of_team(team, o_line_positions).get('average')

            # TODO: Function to get opponent front 7:
            #       Again, depending on the position of player selected, if it's a WR, then heavily weigh the secondary
            #       If it's a RB, heavily weigh the front 7.
            overall_data['opponent_d_front_7_avg'] = get_best_players_of_team(opposing_team_mapped, d_front_7_positions).get('average')
            overall_data['opponent_d_secondary_avg'] = get_best_players_of_team(opposing_team_mapped, d_secondary_positions).get('average')
            overall_data['opposing team'] = opposing_team
            return overall_data


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

