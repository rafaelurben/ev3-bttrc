#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

from multiprocessing import Process

import time

def prepareascii(text):
    return text.replace("Ä", "<AE>").replace("Ö", "<OE>").replace("Ü", "<UE>").replace("ä", "<ae>").replace("ö", "<oe>").replace("ü", "<ue>")


class Morse():
    touch = TouchSensor(INPUT_1)
    display = Display()
    sound = Sound()
    _led = Leds()

    morse_alphabet = {  'A':'.-',       'B':'-...',
                        'C':'-.-.',     'D':'-..',      'E':'.',
                        'F':'..-.',     'G':'--.',      'H':'....',
                        'I':'..',       'J':'.---',     'K':'-.-',
                        'L':'.-..',     'M':'--',       'N':'-.',
                        'O':'---',      'P':'.--.',     'Q':'--.-',
                        'R':'.-.',      'S':'...',      'T':'-',
                        'U':'..-',      'V':'...-',     'W':'.--',
                        'X':'-..-',     'Y':'-.--',     'Z':'--..',
                        'Ä':'.-.-',     'Ö':'---.',     'Ü':'..--',
                        '1':'.----',    '2':'..---',    '3':'...--',
                        '4':'....-',    '5':'.....',    '6':'-....',
                        '7':'--...',    '8':'---..',    '9':'----.',
                        '0':'-----',    ',':'--..--',   '.':'.-.-.-',
                        ':':'---...',   "'":'.----.',   '"':'-.--.-',
                        '?':'..--..',   '/':'-..-.',    '-':'-....-',
                        '@':'.--.-.',   '=':'-...-',    '&':'.-...',
                        '(':'-.--.',    ')':'-.--.-',   '!':'-.-.--',
                        'UNDERSTOOD': '...-.'
                    }
    morse_alphabet_inverted = {v:k for k,v in morse_alphabet.items()}

    @classmethod
    def _setState(self, state):
        setcolor = lambda color: self._led.set_color("LEFT", color.upper())
        if state == "PRESSED":
            setcolor("YELLOW")

        elif state == "IDLE":
            setcolor("ORANGE")

        elif state == "CANCEL":
            setcolor("RED")
            self.sound.beep(args="-l 250")

        elif state == "CHAR_ADDED":
            setcolor("GREEN")
            self.sound.beep(args="-l 50")
            self._setState("IDLE")

        elif state == "SPACE_ADDED":
            setcolor("GREEN")
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")

        elif state == "ERROR":
            setcolor("RED")
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")

        elif state == "END":
            setcolor("GREEN")
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")

        elif state == "DELETE_WORD":
            setcolor("GREEN")
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")
            time.sleep(0.05)
            self.sound.beep(args="-l 50")

        else:
            print("[Morse] - Status nicht gefunden...")

    @classmethod
    def _print(self, text="", char="", message=""):
        print("[Morse] - Text: '"+prepareascii(text)+"' Char: '"+prepareascii(char)+"'"+((" Message: '"+prepareascii(message)+"'") if message else ""))

    @classmethod
    def enterText(self, press_short=0.15, press_timeout=1, rest_short=1, rest_timeout=3):
        self._print("","","Warte auf Code...")

        text = ""
        while True:
            self._setState("IDLE")

            char = ""
            self.touch.wait_for_pressed()
            while True:
                self._setState("PRESSED")
                # Kurz (Punkt)
                if self.touch.wait_for_released(timeout_ms=press_short*1000):
                    self._setState("IDLE")

                    char += "."
                    self._print(text, char, "Kurz!")

                # Lang (Strich)
                else:
                    char += "-"
                    self._print(text, char, "Lang!")

                    # Gedrückt halten
                    if not self.touch.wait_for_released(timeout_ms=(press_timeout-press_short)*1000):
                        self._setState("IDLE")

                        # Charakter zurücksetzen
                        if not char == "":
                            self._print(text, "", "Abbruch!")

                            self._setState("CANCEL")

                            self.touch.wait_for_released()
                        break
                    else:
                        self._setState("IDLE")



                # Kurze Pause
                if self.touch.wait_for_pressed(timeout_ms=rest_short*1000):
                    # Nichts tun
                    pass

                # Lange Pause
                else:
                    # Charakter hinzufügen
                    if char in self.morse_alphabet_inverted:
                        text += self.morse_alphabet_inverted[char]
                        self._print(text, "", "Gefunden: "+self.morse_alphabet_inverted[char])

                        self._setState("CHAR_ADDED")
                        

                    # Ende der Nachricht / Ende der Übertragung
                    elif char == ".-.-." or char == "...-.-":
                        self._print(text, "", "Nachricht beendet!")

                        self._setState("END")
                        return str(text)

                    # Letztes Wort entfernen
                    elif char == "........":
                        text = text.rstrip()
                        while len(text) > 0 and text[-1] != " ":
                            text = text[:-1]
                        self._print(text, "", "Wort geloescht!")

                        self._setState("DELETE_WORD")

                    # Fehler
                    else:
                        self._print(text, char, "Nicht gefunden!!")

                        self._setState("ERROR")

                    # Weiter warten
                    if not self.touch.wait_for_pressed(timeout_ms=(rest_timeout-rest_short)*1000):
                        # Leerzeichen
                        if len(text) > 0 and not text[-1] == " ":
                            text += " "
                            self._print(text, "", "Leerzeichen")

                            self._setState("SPACE_ADDED")

                    # Nächster Charakter
                    break
