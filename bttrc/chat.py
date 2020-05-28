#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

import requests, time, os


def prepareascii(text):
    return text.replace("Ä", "<AE>").replace("Ö", "<OE>").replace("Ü", "<UE>").replace("ä", "<ae>").replace("ö", "<oe>").replace("ü", "<ue>")

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
        url = self.toEV3
        if "error" in requests.get(url).json():
            requests.post(url,  data={"value": ""})

        print("\n[Chat] - Warte auf Erhalt einer Nachricht...")

        while True:
            r = requests.get(url)
            json = r.json()
            if "value" in json and not json["value"] in ["", None]:
                requests.post(url, data={"value": ""})
                print("\n[Chat] - Erhalten: '"+prepareascii(json["value"])+"'")
                return json["value"]
            time.sleep(0.5)

    @classmethod
    def send(self, value):
        url = self.fromEV3
        requests.post(url, data={"value": value or ""})
        print("[Chat] - Gesendet: '"+prepareascii(value)+"'")
