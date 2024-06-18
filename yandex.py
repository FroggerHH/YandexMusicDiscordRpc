from yandex_music import Client

import cfg
from track import Track
from utils import ms_to_sec

if cfg.ym_id: client = Client(cfg.ym_id).init()
else: client = Client()


def get_current_track(local_track_name: str) -> Track or None:
    try:
        track = client.search(text=local_track_name, type_='track')
        track = track.tracks.results[0]
        track = Track(
            [artist.name for artist in track.artists],
            track.title,
            "https://" + track.cover_uri.replace("%%", "1000x1000"),
            f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}",
            ms_to_sec(track.duration_ms),
            track
        )
        return track

    except Exception as e:
        print("An error occurred: ", e)

    return None
