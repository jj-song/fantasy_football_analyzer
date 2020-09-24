import configparser
from runner.utilities.data_loader import load_madden_rating_data, load_injury_data
from runner.extractors.high_awareness_players import get_high_awareness_49ers
from runner.extractors.get_positions import get_best_players
from runner.utilities.data_sorter import list_sort_by_dict_average_value

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

front_7_positions = {
    'LE': 1,
    'RE': 1,
    'DT': 2,
    'LOLB': 1,
    'MLB': 1,
    'ROLB': 1
}

secondary_positions = {
    'SS': 1,
    'FS': 1,
    'CB': 2
}

oline_positions = {
    'LT': 1,
    'LG': 1,
    'C': 1,
    'RG': 1,
    'RT': 1
}


def main():
    # high_awareness_players = get_high_awareness_49ers()

    team_oline = dict()
    team_front_7 = dict()
    team_secondary = dict()

    for team in teams:
        if team == 'Football Team':
            team = 'Redskins'
        else:
            team = team

        team_front_7[team] = get_best_players(team, front_7_positions)
        team_secondary[team] = get_best_players(team, secondary_positions)
        team_oline[team] = get_best_players(team, oline_positions)

    top_front_7_avg = list_sort_by_dict_average_value(team_front_7)
    top_secondary_avg = list_sort_by_dict_average_value(team_secondary)
    top_oline_avg = list_sort_by_dict_average_value(team_oline)

    print("hello")


if __name__ == "__main__":
    load_madden_rating_data()
    load_injury_data()
    #main()
