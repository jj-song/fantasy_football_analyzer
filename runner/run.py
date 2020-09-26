import configparser
from runner.utilities.data_loader import load_player_rating_data, load_injury_data, load_schedule_data
from runner.extractors.get_positions import get_best_players_of_team
from runner.utilities.data_sorter import list_sort_by_dict_average_value
from runner.extractors.get_player_projection import get_player_accessory_data
from runner.utilities.constants import d_front_7_positions,d_secondary_positions,o_line_positions,o_skilled_positions

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

def main():
    # high_awareness_players = get_high_awareness_49ers()


    team_d_front_7 = dict()
    team_d_secondary = dict()
    team_o_line = dict()
    team_o_skilled = dict()
    #assessment_data = dict()

    for team in teams:
        team_d_front_7[team] = get_best_players_of_team(team, d_front_7_positions)
        team_d_secondary[team] = get_best_players_of_team(team, d_secondary_positions)
        team_o_line[team] = get_best_players_of_team(team, o_line_positions)
        team_o_skilled[team] = get_best_players_of_team(team, o_skilled_positions)

    top_d_front_7_avg = list_sort_by_dict_average_value(team_d_front_7)
    top_d_secondary_avg = list_sort_by_dict_average_value(team_d_secondary)
    top_o_line_avg = list_sort_by_dict_average_value(team_o_line)
    top_o_skilled_avg = list_sort_by_dict_average_value(team_o_skilled)

    assessment_data = get_player_accessory_data(team='49ers',player='Jerick McKinnon',week=2)

    print("hello")


if __name__ == "__main__":
    # load_player_rating_data()
    # load_injury_data()
    # load_schedule_data()
    main()
