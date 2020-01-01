# signature fun(msg_sender)
import functools


def command_test(msg_sender, queue, sender_nick):
    msg_sender('testing some stuff')


def command_asdf(msg_sender, queue, sender_nick):
    msg_sender('asdfster')


def vote_fun(msg_sender, queue, sender_nick, vote):
    queue.put_nowait({"nick": sender_nick, "vote": vote})


def init_cmds():
    global COMMANDS

    for i in range(1, 20):
        for j in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s"]:
            sh = j + str(i)
            COMMANDS["#"+sh] = functools.partial(vote_fun, vote=sh)
