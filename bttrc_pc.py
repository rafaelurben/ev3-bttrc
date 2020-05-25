#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben | Matthew Haldimann
#

from multiprocessing import Process
import os, time, requests


class Chat():
    _chaturl = os.getenv("EV3_CHATURL", False)
    _chatkey = os.getenv("EV3_CHATKEY", False)

    if not _chaturl:
        raise EnvironmentError("Missing Environment variable: EV3_CHATURL")
    if not _chatkey:
        raise EnvironmentError("Missing Environment variable: EV3_CHATKEY")

    _chatname = "chat_"+_chatkey+"_"

    geturl = str(_chaturl+_chatname+"fromEV3")
    posturl = str(_chaturl+_chatname+"toEV3")

    @classmethod
    def receive(self):
        if "error" in requests.get(self.geturl).json():
            requests.post(geturl,  data={"value": ""})

        while True:
            r = requests.get(self.geturl)
            json = r.json()
            if "value" in json and not json["value"] in ["", None]:
                requests.post(self.geturl, data={"value": ""})
                return json["value"]
            time.sleep(0.25)

    @classmethod
    def send(self, value):
        if not value in ["", None]:
            requests.post(self.posturl, data={"value": value or ""})
            print("[Gesendet] - "+str(value))

def receive():
    while True:
        print("\n\n[Erhalten] - "+Chat.receive()+"\n")

if __name__ == "__main__":
    print("""
    ---------------------------------------------
    | Back to the roots communication (BTTRC)   |
    | PC-Modul                                  |
    |                                           |
    | 2020 - Rafael Urben                       |
    |                                           |
    | HINWEIS:                                  |
    | Eintrffende Nachrichten löschen           |
    | den Input nicht!                          |
    | (Eingegebener Text wird nur unterbrochen) |
    ---------------------------------------------
    """)

    receiveprocess = Process(target=receive)
    receiveprocess.start()

    while True:
        Chat.send(input("[Senden]: "))
