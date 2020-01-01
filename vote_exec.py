import operator
from queue import Empty
import time

from input_controls import press_w, press_s, press_d, press_a, set_mouse_pos, press_fire, press_r, press_t, press_shift, \
    press_n, press_y, press_1, press_2, press_3, press_i, press_u


def execute_vote(votes):
    vote = max(votes.items(), key=operator.itemgetter(1))[0]
    print(vote)

    if vote == "w":
        press_w()
    elif vote == "s":
        press_s()
    elif vote == "d":
        press_d()
    elif vote == "a":
        press_a()
    elif vote == "0":
        press_fire()
    elif vote == "r":
        press_r()
    elif vote == "t":
        press_t()
    elif vote == "shift":
        press_shift()
    elif vote == "n":
        press_n()
    elif vote == "y":
        press_y()
    elif vote == "1":
        press_1()
    elif vote == "2":
        press_2()
    elif vote == "3":
        press_3()
    elif vote == "i":
        press_i()
    elif vote == "u":
        press_u()
    elif vote == "mouse_up":
        set_mouse_pos(vote)
    elif vote == "mouse_down":
        set_mouse_pos(vote)
    elif vote == "mouse_left":
        set_mouse_pos(vote)
    elif vote == "mouse_right":
        set_mouse_pos(vote)

    return vote


def run_vote(queue, response_queue, txt_updater, config, owner_name):

    current_vote = {}
    viewer_stats = {}

    last_vote_start = time.time()
    time.sleep(1)
    paused = True
    while True:
        td = (time.time() - last_vote_start)
        vote_weight = td / config["vote_time"] + 0.05
        try:
            vote = queue.get(timeout=0.001)

            if not paused and vote["nick"] == owner_name and vote["vote"] == "secret_pause":
                paused = True
            if paused and vote["nick"] == owner_name and vote["vote"] == "secret_run":
                paused = False

            if not paused and vote["vote"] not in ["secret_run", "secret_pause"]:
                count_vote(current_vote, viewer_stats, vote, vote_weight)
        except Empty:
            pass

        if td > config["vote_time"] and not paused:
            print("Checking vote")
            if len(current_vote) > 0:
                response_queue.put_nowait(config["chat_text"] + response)
                response = execute_vote(current_vote)
            current_vote = {}
            last_vote_start = time.time()
        txt_updater.put_nowait({"type": "count", "content": current_vote})
        txt_updater.put_nowait({"type": "stats", "content": viewer_stats})


def count_vote(current_vote, viewer_stats, vote, vote_weight):
    if vote["vote"] not in current_vote:
        current_vote[vote["vote"]] = 0
    current_vote[vote["vote"]] += 1.0 * vote_weight
    if not vote["nick"] in viewer_stats:
        viewer_stats[vote["nick"]] = 0
    viewer_stats[vote["nick"]] += 1
