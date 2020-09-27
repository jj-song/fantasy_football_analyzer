import configparser
from runner.utilities.data_loader import load_player_rating_data, load_injury_data, load_schedule_data, load_all_data
from runner.extractors.get_positions import get_best_players_of_team
from runner.utilities.data_sorter import list_sort_by_dict_average_value
from runner.extractors.get_player_projection import get_player_accessory_data
from runner.utilities.constants import d_front_7_positions,d_secondary_positions,o_line_positions,o_skilled_positions

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

def main():
    # high_awareness_players = get_high_awareness_49ers()


    # team_d_front_7 = dict()
    # team_d_secondary = dict()
    # team_o_line = dict()
    # team_o_skilled = dict()


    # for team in teams:
    #     team_d_front_7[team] = get_best_players_of_team(team, d_front_7_positions)
    #     team_d_secondary[team] = get_best_players_of_team(team, d_secondary_positions)
    #     team_o_line[team] = get_best_players_of_team(team, o_line_positions)
    #     team_o_skilled[team] = get_best_players_of_team(team, o_skilled_positions)
    #
    # top_d_front_7_avg = list_sort_by_dict_average_value(team_d_front_7)
    # top_d_secondary_avg = list_sort_by_dict_average_value(team_d_secondary)
    # top_o_line_avg = list_sort_by_dict_average_value(team_o_line)
    # top_o_skilled_avg = list_sort_by_dict_average_value(team_o_skilled)

    assessment_data = dict()
    # test for RB
    assessment_data['kareem_hunt'] = get_player_accessory_data(team='Browns',player='Kareem Hunt',week=3)
    assessment_data['alvin_kamara'] = get_player_accessory_data(team='Saints', player='Alvin Kamara', week=3)
    assessment_data['derrick_henry'] = get_player_accessory_data(team='Titans', player='Derrick Henry', week=3)

    # test for WR
    assessment_data['marvin_jones'] = get_player_accessory_data(team='Lions', player='Marvin Jones Jr', week=3)
    assessment_data['corey_davis'] = get_player_accessory_data(team='Titans', player='Corey Davis', week=3)
    assessment_data['will_fuller'] = get_player_accessory_data(team='Texans', player='Will Fuller V', week=3)

    # test for QB
    assessment_data['baker_mayfield'] = get_player_accessory_data(team='Browns', player='Baker Mayfield', week=3)
    assessment_data['drew_brees'] = get_player_accessory_data(team='Saints', player='Drew Brees', week=3)
    assessment_data['deshaun_watson'] = get_player_accessory_data(team='Texans', player='Deshaun Watson', week=3)
    assessment_data['patrick_mahomes'] = get_player_accessory_data(team='Chiefs', player='Patrick Mahomes', week=3)

    print("hello")


if __name__ == "__main__":
    #load_all_data()
    main()
