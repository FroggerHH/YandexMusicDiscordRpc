import discord_rpc
import time

import scan
from cfg import config
import utils
from yandex import get_current_track
from track import Track

player_name: str
running = False
cashed_track: Track or None = None
cashed_title = ''
time_started = 0


def on_disconnect(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
        codeno, codemsg))


def on_error(errno, errmsg):
    print('An error occurred! Error {}: {}'.format(errno, errmsg))


def shutdown():
    global player_name, running
    print("Player stopped ending session...")
    player_name = ''
    running = False
    discord_rpc.shutdown()


def main_loop():
    global running, player_name
    while True:
        if player_name:
            while running:
                update()
                time.sleep(config.sleep_time)
            shutdown()
        else:
            while not running:
                print("Waiting for player...")
                player_name = scan.check_players()
                running = True if player_name else False

                if running:
                    print("Opening session on player", player_name)
                    run_discord_rpc()

                time.sleep(config.sleep_time)


def update():
    global player_name, cashed_track, cashed_title, running, time_started
    act_players = utils.execute("playerctl -l").split('\n')
    if player_name not in act_players:
        running = False
        return

    title = utils.execute('playerctl -p ' + player_name + " metadata --format \"{{title}}\"")
    if not title: return
    position = int(float(utils.execute('playerctl -p ' + player_name + " position")))

    if cashed_title == title:
        track = cashed_track
    else:
        artists = utils.execute('playerctl -p ' + player_name + " metadata --format \"{{artist}}\"")
        track = get_current_track(title, artists)
        time_started = time.time() - position

    cashed_title = title
    cashed_track = track

    if track is None: return

    args = dict(
        details=f'{track.name}',
        state=progress_bar(position, track.duration_sec),
        large_image_key=track.preview,
        large_image_text='' + (
            f'Исполнители: {", ".join(track.artists)}' if config.show_artists_on_hover_large else '')
                         + (f' Трек:{track.name}' if config.show_title_on_hover_large else ''),
        small_image_key='yandex-music',
        start_timestamp=time_started if config.show_time else 0,
        end_timestamp=(time_started + track.duration_sec) if config.show_time else 0,
    )

    discord_rpc.update_presence(**args)

    # # Вывод дебаг информации о треке
    # print("Current track: " + track.name)
    # print("Artists: " + ', '.join(track.artists))
    # print("Preview: " + track.preview)
    # print("Link: " + track.link)
    # print("Duration: " + str(track.duration_sec))
    # print("--------------------------")

    discord_rpc.update_connection()
    time.sleep(2)
    discord_rpc.run_callbacks()


def progress_bar(elapsed_time, duration):
    # Вычисляем прогресс
    progress_ratio = min(max(elapsed_time / duration, 0), 1)  # Прогресс от 0 до 1

    # Вычисляем количество символов для заполненной части прогресс-бара
    filled_length = int(config.bar_length * progress_ratio)

    # Формируем прогресс-бар
    bar = f'>' + '•' * filled_length + '-' * (config.bar_length - filled_length) + '<'
    if config.show_time_on_bar:
        bar = utils.format_time(elapsed_time) + bar + utils.format_time(duration)

    return bar


changeTimeDict = {
    0: 1,
    1: 60,
    2: 3600,
    3: 86400,
}


def run_discord_rpc():
    callbacks = {'disconnected': on_disconnect, 'error': on_error}
    discord_rpc.initialize(app_id="1251194032881799191", callbacks=callbacks, log=True, log_file="discord_log.txt")


def startup(player: str or None):
    global player_name, running, time_started, cashed_track, cashed_title
    time_started = time.time()
    cashed_track = None
    cashed_title = ''

    if player:
        print("Opening session on player", player)
        player_name = player
        running = True
        run_discord_rpc()
    else:
        player_name = ''
        running = False

    main_loop()
