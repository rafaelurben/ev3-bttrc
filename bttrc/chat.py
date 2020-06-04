#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

import requests, time, os
from ev3dev2.sound import Sound


def prepareascii(text):
    return text.replace("Ä", "<AE>").replace("Ö", "<OE>").replace("Ü", "<UE>").replace("ä", "<ae>").replace("ö", "<oe>").replace("ü", "<ue>")

class Chat():
    _sound = Sound()
    _chaturl = os.getenv("EV3_CHATURL", False)
    _chatkey = os.getenv("EV3_CHATKEY", False)

    if not _chatkey or not _chaturl:
        _env = {}
        try:
            with open(os.path.join(os.getcwd(),".env"), mode="r") as file:
                for line in file:
                    _env[line.split("=")[0]] = line.split("=")[1]

            if not _chatkey:
                if "EV3_CHATKEY" in _env:
                    _chatkey = _env["EV3_CHATKEY"]
                else:
                    raise EnvironmentError("Environment variable missing: EV3_CHATKEY")

            if not _chaturl:
                if "EV3_CHATURL" in _env:
                    _chaturl = _env["EV3_CHATURL"]
                else:
                    _chaturl = "https://rafaelurben.herokuapp.com/onlinevars/api/v1/"

        except FileNotFoundError:
            pass

    toEV3 = str(_chaturl+"chat_"+_chatkey+"_toEV3")
    fromEV3 = str(_chaturl+"chat_"+_chatkey+"_fromEV3")

    @classmethod
    def receive(self):
        try:
            url = self.toEV3
            print("[Chat] - Bereit!")

            while True:
                json = requests.get(url+"?create=true&clean=true").json()
                if "value" in json and not json["value"] in ["", None]:
                    print("\n[Chat] - Erhalten: '"+prepareascii(json["value"])+"'")
                    try:
                        self._sound.play_file("/home/robot/ev3-bttrc/files/message_received.wav")
                    except Exception as e:
                        pass
                    return json["value"]
                time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print("[Chat] - Error:", e)
            try:
                self._sound.play_file("/home/robot/ev3-bttrc/files/message_error.wav")
            except Exception as e:
                pass
            return "CHAT NICHT VERFÜGBAR"

    @classmethod
    def send(self, value):
        try:
            url = self.fromEV3
            requests.post(url, data={"value": value or "", "append": True})

            print("[Chat] - Gesendet: '"+prepareascii(value)+"'")
            try:
                self._sound.play_file("/home/robot/ev3-bttrc/files/message_sent.wav")
            except Exception as e:
                pass
            return True
        except requests.exceptions.RequestException as e:
            print("[Chat] - Error:", e)
            try:
                self._sound.play_file("/home/robot/ev3-bttrc/files/message_error.wav")
            except Exception as e:
                pass
            return False
