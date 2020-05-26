#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben | Matthew Haldimann
#

from bttrc import Chat, Morse, Printer
from multiprocessing import Process
import time

def processQueue():
    Printer.processQueue()

def morse2chat():
    while True:
        Chat.send(Morse.enterText())

def chat2print():
    while True:
        Printer.addToQueue(Chat.receive()+"\n")

if __name__ == "__main__":
    printprocess = Process(target=processQueue)
    printprocess.start()

    chat2printprocess = Process(target=chat2print)
    chat2printprocess.start()

    morse2chat()

    print("[BTTRC] - Beenden...")

    printprocess.terminate()
    chat2printprocess.terminate()

    print("[BTTRC] - Beendet!")
