# vk-tg-suckling-user-bot

This is one-way bridge for messages from vkontakte to telegram (hence
"suckling", it sucks (messages) from vk).

This is user bot, meaning that it uses user auth tokens. I don't know does it
work with group tokens because I don't have one. But probably it should works
too.

## Setup

Rename `config.py.example` to `config.py` and edit its content according to the
template.

Run bot:

```
python main.py
```

Or if you running it on server, you may want use script that write logs to file
and restarts bot if it fails (but be careful: it will still infinitely
restarting if you have syntax errors in config file):

```
./run_bot_vk_tg.sh
```
