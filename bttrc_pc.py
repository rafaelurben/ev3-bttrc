#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben 
#

import requests, time, os

class Chat():
    _chaturl = os.getenv("EV3_CHATURL", "https://rafaelurben.herokuapp.com/onlinevars/api/v1/")
    _chatkey = os.getenv("EV3_CHATKEY", False)

    if not _chatkey:
        raise EnvironmentError("Missing Environment variable: EV3_CHATKEY")

    _chatname = "chat_"+_chatkey+"_"

    toEV3 = str(_chaturl+_chatname+"toEV3")
    fromEV3 = str(_chaturl+_chatname+"fromEV3")

    @classmethod
    def receive(self):
        url = self.fromEV3
        if "error" in requests.get(url).json():
            requests.post(url,  data={"value": ""})

        print("\n[Chat] - Warte auf Erhalt einer Nachricht...")

        while True:
            r = requests.get(url)
            json = r.json()
            if "value" in json and not json["value"] in ["", None]:
                requests.post(url, data={"value": ""})
                print("\n[Chat] - Erhalten: '"+json["value"]+"'")
                return json["value"]
            time.sleep(0.5)

    @classmethod
    def send(self, value):
        url = self.toEV3
        requests.post(url, data={"value": value or ""})
        print("[Chat] - Gesendet: '"+value+"'")


from multiprocessing import Process

def receive():
    while True:
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

    time.sleep(2.5)

    while True:
        Chat.send(input("[Chat] - Senden: "))
