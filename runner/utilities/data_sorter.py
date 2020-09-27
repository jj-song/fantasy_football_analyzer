def list_sort_by_dict_value(players, value):
    """
    This function gathers player data using the madden rating API.
    The player data is saved under their respective team json files.
    """
    players = sorted(players.items(), key=lambda x: x[1][value], reverse=True)
    return players