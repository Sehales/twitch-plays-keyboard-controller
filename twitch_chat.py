import functools
import re
import socket


import select
from queue import Empty


def send_pong(msg, con):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, con, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick, con):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password, con):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan, con):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan,con):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg, sender, queue, sender_nick, commands):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = commands
        if msg[0] in options:
            options[msg[0]](sender, queue, sender_nick)


def establish_connection(config):
    con = socket.socket()

    con.connect((config["credentials"]["host"], config["credentials"]["port"]))
    con.setblocking(0)

    send_pass(config["credentials"]["oauth"], con)
    send_nick(config["credentials"]["nickname"], con)
    join_channel(config["credentials"]["channel"], con)
    return con


def run_twitch_chat(queue, resp_queue, commands, config):
    con = establish_connection(config)
    data = ""

    while True:

        try:
            ready = select.select([con], [], [], 0.01)
            if ready[0]:
                data = data + con.recv(2048).decode('UTF-8')

            data_split = re.split(r"[~\r\n]+", data)
            data = data_split.pop()

            for line in data_split:
                line = str.rstrip(line)
                line = str.split(line)

                if len(line) >= 1:
                    if line[0] == 'PING':
                        send_pong(line[1], con)
                        print("Ponging!")

                    if line[1] == 'PRIVMSG':
                        sender = get_sender(line[0])
                        message = get_message(line)
                        parse_message(message, functools.partial(send_message, config["credentials"]["channel"], con), queue, sender, commands)

                        print(sender + ": " + message)

        except socket.error:
            print("Socket died - retrying")
            con = establish_connection(config)
        try:
            response = resp_queue.get(timeout=0.001)
            send_message(config["credentials"]["channel"], con, response)
        except Empty:
            pass