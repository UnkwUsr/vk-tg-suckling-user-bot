# vk-tg-suckling-user-bot

This is one-way bridge for chat messages from vkontakte to telegram (hence
"suckling", it sucks (messages) from vk).

This is user bot, meaning that it uses user auth token. I don't know if it
works with group tokens because I don't have one, but probably it should works
too.

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
