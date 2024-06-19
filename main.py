import cfg
from yandex_music.track.track import Track
import utils
from time import sleep, time
import session
import atexit
atexit.register(session.shutdown)

trackTime: float = None
lastTrack: Track = None

busy_session: session.Session = None


def check_players():
    # check if already busy with a session
    global busy_session
    if busy_session is not None: return False
    # Check if any players are playing
    act_players = utils.execute("playerctl -l").split('\n')
    print('Players: ', act_players)
    for player_name in act_players:
        if player_name.startswith('chromium.instance'):
            # try:
            if busy_session and busy_session.player_name == player_name: return True
            busy_session = session.Session(player_name)
            print("Session started")
            return True
            # except:
            #     print("An error occured, restarting...")
    busy_session = None
    print("No player found")


def main():
    global lastTrack, trackTime

    while True:
        check_players()
        sleep(cfg.sleep_time)


# Запуск
if __name__ == "__main__":
    main()
