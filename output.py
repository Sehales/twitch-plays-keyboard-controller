from queue import Empty


_VIEWER_COUNT = "./vote_stats.txt"
_CURRENT_VOTE = "./current_vote.txt"


def run_txt_updater(queue):

    while True:
        try:
            text_updater = queue.get(timeout=5.5)

            if text_updater["type"] == "count":
                file = _CURRENT_VOTE
            else:
                file = _VIEWER_COUNT

            with open(file, "w+") as f:
                f.write(str(text_updater["content"]).replace("{", "").replace("}", ""))

        except Empty:
            pass