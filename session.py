import discord_rpc
import time
import cfg
import utils
from yandex import get_current_track


def on_disconnect(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
        codeno, codemsg))


def on_error(errno, errmsg):
    print('An error occurred! Error {}: {}'.format(errno, errmsg))


def shutdown():
    print("Player stopped ending session...")
    discord_rpc.shutdown()


class Session:
    def __init__(self, player_name: str) -> None:
        print("Opening session on player")

        callbacks = {'disconnected': on_disconnect, 'error': on_error}
        discord_rpc.initialize(app_id="1251194032881799191", callbacks=callbacks, log=True, log_file="discord_log.txt")

        self.details = "Initializing player "
        self.state = "state"
        self.player_name = player_name

        self.running = True

        while self.running:
            self.update()
            time.sleep(cfg.sleep_time)
        shutdown()

    def update(self):
        title = utils.execute('playerctl -p ' + self.player_name + " metadata --format \"{{title}}\"")
        if not title: return
        artists = utils.execute('playerctl -p ' + self.player_name + " metadata --format \"{{artist}}\"")
        position = int(float(utils.execute('playerctl -p ' + self.player_name + " position")))

        track = get_current_track(title, artists)
        if track is None: return

        discord_rpc.update_presence(
            **{
                'details': f'{track.name}',
                'state': progress_bar(position, track.duration_sec),
                'large_image_key': track.preview,
                'large_image_text': f'Исполнители: {", ".join(track.artists)} \n\nТрек: {track.name}',
                'small_image_key': 'yandex-music',
            })

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
    total_length = 20  # Длина прогресс-бара без границ
    filled_length = int(total_length * progress_ratio)

    # Формируем прогресс-бар
    bar = '>' + '•' * filled_length + '-' * (total_length - filled_length) + '<'

    return bar


def change_time(_time: str):
    t1 = _time.split(":")
    result = 0
    for i in range(len(t1)):
        result += int(t1[-(i + 1)]) * changeTimeDict[i]
    return result


changeTimeDict = {
    0: 1,
    1: 60,
    2: 3600,
    3: 86400,
}
