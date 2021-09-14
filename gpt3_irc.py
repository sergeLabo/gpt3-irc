
#! /usr/bin/env python3


"""
It also responds to DCC CHAT invitations and echos data sent in such
sessions.
    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

import random
from time import time, sleep
import textwrap

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr


class GPT3IrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, realname, server, port):
        super().__init__([(server, port)], nickname, realname)
        self.channel = channel
        self.question = "Who are you?"
        self.response = "I'm stupid"
        self.num = 0
        self.quest_rep = {}
        self.alive = 1

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        print("on_nicknameinuse")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("Welcome on #lalabomedia IRC")

    def on_pubmsg(self, c, e):

        # a est le messge reçu
        msg = e.arguments[0].split(":", 1)

        i_am = irc.strings.lower(self.connection.get_nickname())
        # Si le message commence par "TheGeneral: "
        if len(msg) > 1 and irc.strings.lower(msg[0]) == i_am:
            # La commande est la suite de "TheGeneral: texte_du_message
            self.do_command(e, msg[1].strip())

    def do_command(self, e, cmd):

        self.question = cmd.lower()
        self.quest_rep[self.num] = [self.question]
        while len(self.quest_rep[self.num]) == 1:
            sleep(0.01)
        if len(self.quest_rep[self.num]) == 2:
            msg = [self.quest_rep[self.num][0],
                    self.quest_rep[self.num][1]]
            self.send_pubmsg(msg)
            self.num += 1

    def send_pubmsg(self, msg):
        self.connection.privmsg("#lalabomedia", "Q: " + msg[0])
        sleep(0.1)
        self.connection.privmsg("#lalabomedia", "R: " + msg[1])


def gpt3_irc_bot_main():

    server = "irc.libera.chat"
    port = 6667
    channel = "#lalabomedia"
    nickname = "gpt3"
    realname = "OpenAI GPT-3"

    bot = GPT3IrcBot(channel, nickname, realname, server, port)
    bot.start()




if __name__ == "__main__":
    gpt3_irc_bot_main()


