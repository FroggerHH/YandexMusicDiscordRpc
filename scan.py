import utils


def check_players():
    act_players = utils.execute("playerctl -l").split('\n')
    print('Players: ', act_players)

    for player_name in act_players:
        if player_name.startswith('chromium.instance'):
            return player_name

    return ''
