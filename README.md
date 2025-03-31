# vk-tg-suckling-user-bot

This is one-way bridge for chat messages from vkontakte to telegram (hence
"suckling", it sucks (messages) from vk, and only this way).

You can make multiple different chat bridges, selecting from which vk chat to
take messages and to which telegram chat bridge them.

This is user bot, meaning that it uses user auth token. I don't know if it
works with group tokens because I don't have one, but probably it should works
too.

## Supported attachments

* [x] reply messages
* [x] forwarded messages
* [x] images
* [x] voice messages
* [x] documents (aka files)
* [x] stickers
* [x] graffiti
* [x] links
* [x] wall posts
* [x] comments to wall posts
* [x] video (reuploads video files to telegram (by default limited to 3 minutes
  video duration))

not planned:

* music (user token have not enough permissions)
* stories (user token have not enough permissions)

## Running

Preparation step: rename `config.py.example` to `config.py` and edit it
according to the template.

### docker compose

```
docker-compose up
```

### Manual

Install dependencies:

```
pip install -r requirements.txt
```

Run bot:

```
python main.py
```

Or if you running it on server, you may want to use script that write logs to
file and automatically restarts if bot crashes (but be careful: it will still
infinitely restarting if you have syntax errors in config file):

```
./run_bot_vk_tg.sh
```

## License notice

```
Copyright (C) 2023 UnkwUsr

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```
