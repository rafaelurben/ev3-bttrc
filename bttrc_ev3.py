#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben | Matthew Haldimann
#

from BTTRC import Chat, Morse, Printer
from multiprocessing import Process
import os, time

def morse2chat():
    while True:
        Chat.send(Morse.enterText())

def chat2print():
    while True:
        Printer.addToQueue(Chat.receive()+"\n")

if __name__ == "__main__":
    printprocess = Process(target=Printer.processQueue)
    printprocess.start()

    chat2printprocess = Process(target=chat2print)
    chat2printprocess.start()

    morse2chatprocess = Process(target=morse2chat)
    morse2chatprocess.start()

    # idle
    morse2chatprocess.join()
