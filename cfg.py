# Конфигурация
import dataclasses
import json
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import atexit


def shutdown():
    print("Stopping config file watcher...")


atexit.register(shutdown)


@dataclasses.dataclass
class Config:
    # Интервал обновления информации о треке в секундах
    sleep_time: int = 3
    # Показывать ли длительность трека
    show_time: bool = True
    # Показывать ли длительность трека в дискорде на прогресс-баре
    show_time_on_bar: bool = False
    # Длина прогресс-бара
    bar_length: int = 20
    # Показывать ли исполнителей при наведении на большую картинку
    show_artists_on_hover_large: bool = True
    # Показывать ли название трека при наведении на большую картинку
    show_title_on_hover_large: bool = False

    def read_config(self):
        print('Reading config...')
        with open(path) as f:
            json_data = json.load(f)
            self.sleep_time = json_data['sleep_time']
            self.show_time = json_data['show_time']
            self.show_time_on_bar = json_data['show_time_on_bar']
            self.bar_length = json_data['bar_length']
            self.show_artists_on_hover_large = json_data['show_artists_on_hover_large']
            self.show_title_on_hover_large = json_data['show_title_on_hover_large']


config: Config = Config()
path = 'config.json'

if not os.path.isfile(path):
    with open(path, 'w') as f:
        json.dump(dataclasses.asdict(config), f)
else:
    config.read_config()

# Setup file watcher on file. Call load_config on change
event_handler = FileSystemEventHandler()
event_handler.on_modified = lambda event: config.read_config()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

# Токены

app_id = 1251194032881799191
# ID приложения дискорд, можно не менять

# api токен Яндекс Музыки
# ym_id = "y0_AgAAA********"
# можно и без него, но хз, если надо пропиши свой токен


ym_id = None
