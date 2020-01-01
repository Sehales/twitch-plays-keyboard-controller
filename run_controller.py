import functools
import threading
from queue import Queue

from load_config import load_config, create_config
from output import run_txt_updater
from twitch_chat import run_twitch_chat
from vote_exec import run_vote

if __name__ == "__main__":
    config = load_config("config.json")
    c = create_config(config)
    queue = Queue()
    response_queue = Queue()
    txt_update_queue = Queue()
    twitch_chat_thread = threading.Thread(target=functools.partial(run_twitch_chat, queue, response_queue, c, config))
    voting_thread = threading.Thread(target=functools.partial(run_vote, queue, response_queue, txt_update_queue, config["customize"], config["credentials"]["nickname"]))
    text_thread = threading.Thread(target=functools.partial(run_txt_updater, txt_update_queue))
    threads = [twitch_chat_thread, voting_thread, text_thread]

    print("Starting!")

    for t in threads:
        t.start()

    for t in threads:
        t.join()
