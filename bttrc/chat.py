#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

import requests
import time
import os

class Chat():
    _chaturl = os.getenv("EV3_CHATURL", False)
    _chatkey = os.getenv("EV3_CHATKEY", False)

    if not _chaturl:
        raise EnvironmentError("Missing Environment variable: EV3_CHATURL")
    if not _chatkey:
        raise EnvironmentError("Missing Environment variable: EV3_CHATKEY")

    _chatname = "chat_"+_chatkey+"_"

    geturl = str(_chaturl+_chatname+"toEV3")
    posturl = str(_chaturl+_chatname+"fromEV3")

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
        requests.post(self.posturl, data={"value": value or ""})
