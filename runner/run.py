import configparser
from runner.utilities.data_loader import load_madden_rating_data, load_injury_data, load_schedule_data
from runner.extractors.high_awareness_players import get_high_awareness_49ers
from runner.extractors.get_positions import get_best_players
from runner.utilities.data_sorter import list_sort_by_dict_average_value

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

d_front_7_positions = {
    'LE': 1,
    'RE': 1,
    'DT': 2,
    'LOLB': 1,
    'MLB': 1,
    'ROLB': 1
}

d_secondary_positions = {
    'SS': 1,
    'FS': 1,
    'CB': 2
}

o_line_positions = {
    'LT': 1,
    'LG': 1,
    'C': 1,
    'RG': 1,
    'RT': 1
}

o_skilled_positions = {
    'HB': 2,
    'WR': 2,
    'QB': 1,
    'TE': 1
}


def main():
    # high_awareness_players = get_high_awareness_49ers()


    team_d_front_7 = dict()
    team_d_secondary = dict()
    team_o_line = dict()
    team_o_skilled = dict()

    for team in teams:
        if team == 'Football Team':
            team = 'Redskins'
        else:
            team = team

        team_d_front_7[team] = get_best_players(team, d_front_7_positions)
        team_d_secondary[team] = get_best_players(team, d_secondary_positions)
        team_o_line[team] = get_best_players(team, o_line_positions)
        team_o_skilled[team] = get_best_players(team, o_skilled_positions)

    top_d_front_7_avg = list_sort_by_dict_average_value(team_d_front_7)
    top_d_secondary_avg = list_sort_by_dict_average_value(team_d_secondary)
    top_o_line_avg = list_sort_by_dict_average_value(team_o_line)
    top_o_skilled_avg = list_sort_by_dict_average_value(team_o_skilled)

    print("hello")


if __name__ == "__main__":
    #load_madden_rating_data()
    #load_injury_data()
    load_schedule_data()
    #main()
