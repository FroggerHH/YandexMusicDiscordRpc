from dataclasses import dataclass
from typing import List
from yandex_music.track.track import Track as TrackYandex


@dataclass
class Track:
    artists: List[str]
    name: str
    preview: str
    link: str
    duration_sec: int
    track: TrackYandex