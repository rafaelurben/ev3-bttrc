#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben 
#

import os, time

os.environ['EV3_PC'] = "True"

from bttrc.chat import Chat
from multiprocessing import Process

def receive():
    while True:
        print("\n\n")
        Chat.receive()
        print("\n")

if __name__ == "__main__":
    print("""
    ---------------------------------------------
    | Back to the roots communication (BTTRC)   |
    | PC-Modul                                  |
    |                                           |
    | 2020 - Rafael Urben                       |
    |                                           |
    | HINWEIS:                                  |
    | Eintreffende Nachrichten löschen          |
    | den Input nicht!                          |
    | (Eingegebener Text wird nur unterbrochen) |
    ---------------------------------------------
    """)

    receiveprocess = Process(target=receive)
    receiveprocess.start()

    while True:
        Chat.send(input("[Chat] - Senden: "))
