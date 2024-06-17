from yandex_music import Client
from cfg import ym_id
from track import Track
from utils import ms_to_sec

client = Client(ym_id).init()

def get_current_track():
    queues = client.queues_list()

    # if len(queues) == 0: return None
    # currentQueue = client.queue(queue_id=queues[0].id)
    # currentTrack = currentQueue.get_current_track()
    # aboutTrack = currentTrack.fetch_track()

    aboutTrack = client.users_likes_tracks()[0].fetch_track()

    return Track(
        [artist.name for artist in aboutTrack.artists],
        aboutTrack.title,
        "https://" + aboutTrack.cover_uri.replace("%%", "1000x1000"),
        f"https://music.yandex.ru/album/{aboutTrack.albums[0].id}/track/{aboutTrack.id}",
        ms_to_sec(aboutTrack.duration_ms),
        aboutTrack
    )
