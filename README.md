# YandexMusicDiscordRpc

Отображает в дискорде трек и плейер из десктопного приложения Яндекс.Музыка. <br>
Протестировано на ArchLinux с [yandex-music-linux](https://aur.archlinux.org/packages/yandex-music)

Оно работает!...ну как минимум у меня.

За основу были взяты эти проекты:
* [music-rpc](https://github.com/bramtechs/music-rpc)
* [YoutubeMusicDiscordRPC](https://github.getafreenode.com/ludals/YoutubeMusicDiscordRPC)

Для поиска пести в яндекс.музыке можно используется библиотека 
[yandex-music-api](https://github.com/MarshalX/yandex-music-api)

Работает без каких либо токенов, но при знаии и желании можно указать токен яндекс.музыки в конфиге.

Конфиг в файле `cfg.py`

Скрин: <br>
<img alt="Example.png" width="400" src="Example.png" />

## Использование

### Установка
1. `yay install extra/playerctl`.
2. `git clone https://github.com/FroggerHH/YandexMusicDiscordRpc.git`
3. `cd YandexMusicDiscordRpc`
4. `pip install -r requirements.txt`

### Запуск
`python main.py`


## Известные проблемы
* Не работет с Vesktop
* Обложка песни в дискорде в редких случаях может не совпадать с обложкой в плеере Яндекс.Музыки


### Если у вас что-то не работет, то напишите мне в discord `justafrogger`, постараюсь помочь.

## А если у вас всё работает, влепите звёздочку 🌟 на гите 🥺 