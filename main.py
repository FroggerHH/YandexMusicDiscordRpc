from cfg import sleep_time
from yandex_music.track.track import Track
from yandex import get_current_track
from time import sleep, time
import session
import atexit 


import global_var as gl

trackTime: float = None
lastTrack: Track = None

rpc = session.Session()
atexit.register(rpc.shutdown)

def main():
    global lastTrack, trackTime

    # TODO: Корректный выход из цикла
    while True:
        # Получение текущего трека
        currentTrack = get_current_track()
        if currentTrack is None: 
            print("Трек не обнаружен")
            sleep(cfg.sleepTime)
            continue
        
        currentTime = time()
        if lastTrack is None or lastTrack != currentTrack:
            lastTrack = currentTrack
            trackTime = currentTime
        remainingTime = int(currentTrack.duration_sec - (currentTime - trackTime))

        gl.lastTrack = lastTrack
        gl.trackTime = trackTime
        gl.currentTrack = currentTrack
        gl.remainingTime = remainingTime

        # Вывод дебаг информации о треке
        print("Current track: " + currentTrack.name)
        print("Artists: " + ', '.join(currentTrack.artists))
        print("Preview: " + currentTrack.preview)
        print("Link: " + currentTrack.link)
        print("Duration: " + str(currentTrack.duration_sec))
        print("currentTime: " + str(currentTime))
        print("trackTime: " + str(trackTime))
        print("Remaining time: " + str(remainingTime))
        print("Remaining time: " + str(session.changeTime('01:05')))
        print("--------------------------")
    
        rpc.update()
        # TODO: Изменить на cfg.sleepTime
        sleep(3)

# Запуск
if __name__ == "__main__":
    main()