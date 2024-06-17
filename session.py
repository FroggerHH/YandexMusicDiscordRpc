import discord_rpc
import time
import utils
import global_var as gl

config = [{
     "appID": "1251194032881799191",
     "logo": "logo",
     "Paused": "pause",
     "Playing": "play",
     "Stopped": "stop"
    }]

def on_disconnect(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
        codeno, codemsg))
def on_error(errno, errmsg):
    print('An error occurred! Error {}: {}'.format(errno, errmsg))

class Session:
    def __init__(self) -> None:
        print("Opening session on player")

        callbacks = {'disconnected': on_disconnect, 'error': on_error}
        discord_rpc.initialize(app_id="1251194032881799191", callbacks=callbacks, log=True, log_file="discord_log.txt")
        
        self.details = "Initializing player "
        self.state = "state"
        self.side = False

    def shutdown(self):
        print ("Player stopped ending session...")
        discord_rpc.shutdown()

    def update(self):
        discord_rpc.update_presence(
                **{
                    'details': f'{gl.currentTrack.name}',
                    'state': progress_bar(gl.trackTime, gl.currentTrack.duration_sec),
                    'large_image_key': gl.currentTrack.preview,
                    'large_image_text': f'Исполнители: {", ".join(gl.currentTrack.artists)}\nТрек: {gl.currentTrack.name}',
                    'small_image_key': 'yandex-music',
                    # 'start_timestamp': gl.trackTime,
                    # 'end_timestamp': gl.trackTime + gl.currentTrack.duration_sec,
                })

        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

import time

def progress_bar(start_time, duration):
    current_time = time.time()
    duration = duration
    
    # Вычисляем прогресс
    elapsed_time = current_time - start_time
    progress_ratio = min(max(elapsed_time / duration, 0), 1)  # Прогресс от 0 до 1
    
    # Вычисляем количество символов для заполненной части прогресс-бара
    total_length = 20  # Длина прогресс-бара без границ
    filled_length = int(total_length * progress_ratio)
    if filled_length == 0: filled_length = 1
    
    # Формируем прогресс-бар
    # TODO: Показывать длительность вместь конечного <!
    progress_bar = '!>' + '•' * (filled_length - 1) + '♦' + '-' * (total_length - filled_length) + '<!'
    
    return progress_bar

def changeTime(time: str):
    t1 = time.split(":")
    result = 0
    for i in range(len(t1)):
        result += int(t1[-(i+1)]) * changeTimeDict[i]
    return result

changeTimeDict = {
    0 : 1,
    1 : 60, 
    2 : 3600, 
    3 : 86400, 
}