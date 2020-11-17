import configparser
from runner.utilities.data_loader import load_player_rating_data, load_injury_data, load_schedule_data, load_all_data
from runner.extractors.get_positions import get_best_players_of_team, get_all_players_on_team
from runner.utilities.data_sorter import list_sort_by_dict_value
from runner.extractors.ranked_lists import get_ranked_team_group_positions, get_ranked_positions
from runner.extractors.get_player_projection import get_player_accessory_data
from runner.utilities.constants import d_front_7_positions,d_secondary_positions,o_line_positions,o_skilled_positions,fantasy_positions

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

def main():
    top_d_front_7_avg, top_d_secondary_avg, top_o_line_avg, top_o_skilled_avg = \
        get_ranked_team_group_positions()

    top_qb, top_wr, top_rb = get_ranked_positions()

    print("hello")


if __name__ == "__main__":
    #load_all_data()
    main()
