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
        txt = Chat.receive()
        if not "//NOPRINT//" in txt:
            Printer.addToQueue(txt.rstrip())
            Printer.addToQueue(" ")
        Chat.send("[BTTRC] - Nachricht erhalten!", nosound=True)


if __name__ == "__main__":
    from ev3dev2.button import Button
    from ev3dev2.led import Leds

    l = Leds()
    b = Button()

    l.all_off()
    l.set_color("LEFT",  "RED")
    l.set_color("RIGHT", "RED")

    print("[BTTRC] - Starten...")

    printprocess = Process(target=processQueue)
    printprocess.start()

    chat2printprocess = Process(target=chat2print)
    chat2printprocess.start()

    morse2chatprocess = Process(target=morse2chat)
    morse2chatprocess.start()

    Chat.send("[BTTRC] - Gestartet!", nosound=True)

    print("[BTTRC] - Gestartet!")

    b.wait_for_bump("left")

    print("[BTTRC] - Beenden...")

    printprocess.terminate()
    chat2printprocess.terminate()
    morse2chatprocess.terminate()

    Chat.send("[BTTRC] - Beendet!", nosound=True)

    print("[BTTRC] - Beendet!")

    l.all_off()
