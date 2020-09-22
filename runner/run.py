import configparser
from runner.utilities.data_loader import load_data
from runner.extractors.high_awareness_players import get_high_awareness_49ers
from runner.extractors.get_positions import get_best_team_oline

config = configparser.ConfigParser()
config.read(r'C:\Users\Jihoon\Documents\Projects\fantasy_football_analyzer\local.ini')
teams = list(config['constants']['teams'].split(","))

def main():
    high_awareness_players = get_high_awareness_49ers()
    #nfl_oline = get_entire_nfl_oline()

    team_oline = dict()
    for team in teams:
        if team == 'Football Team':
            team = 'Redskins'
        else:
            team = team
        team_oline[team] = get_best_team_oline(team)


    team_oline = sorted(team_oline.items(), key=lambda x: x[1]['average'], reverse=True)

    print("hello")

if __name__ == "__main__":
    #load_data()
    main()
