

def list_sort_by_dict_average_value(players):
    """
    This function gathers player data using the madden rating API.
    The player data is saved under their respective team json files.
    """
    players = sorted(players.items(), key=lambda x: x[1]['average'], reverse=True)
    return players
