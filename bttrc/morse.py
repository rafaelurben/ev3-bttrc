#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.display import Display
from ev3dev2.sound import Sound

from multiprocessing import Process

import time

class Morse():
    touch = TouchSensor(INPUT_1)
    display = Display()
    sound = Sound()

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
    def _print(self, text="", char="", message=""):
        print("[Morse] - Text: '"+text+"' Char: '"+char+"'"+((" Message: '"+message+"'") if message else ""))


    @classmethod
    def enterText(self, press_short=0.25, press_long=1, rest_short=1, rest_long=3):
        self._print("","","Warte auf Code...")
        self.display.text_grid(text="Warte auf Code...", x=0, y=0,  font="luBS14", clear_screen=True)
        self.display.update()

        text = ""
        while True:
            char = ""
            self.touch.wait_for_pressed()
            while True:
                # Kurz (Punkt)
                if self.touch.wait_for_released(timeout_ms=press_short*1000):
                    char += "."
                    self._print(text, char, "Kurz!")

                # Lang (Strich)
                else:
                    char += "-"
                    self._print(text, char, "Lang!")

                    # Gedrückt halten
                    if not self.touch.wait_for_released(timeout_ms=(press_long-press_short)*1000):
                        # Charakter zurücksetzen
                        if not char == "":
                            self._print(text, "", "Abbruch!")

                            # TODO: Cancel-Sound
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")

                            self.touch.wait_for_released()
                        break



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

                        # TODO: Char-Sound
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")

                    # Ende der Nachricht / Ende der Übertragung
                    elif char == ".-.-." or char == "...-.-":
                        self._print(text, "", "Nachricht beendet!")

                        # TODO: Ende-Sound
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        return str(text)

                    # Letztes Wort entfernen
                    elif char == "........":
                        text = text.rstrip()
                        while len(text) > 0 and text[-1] != " ":
                            text = text[:-1]
                        self._print(text, "", "Wort geloescht!")

                        # TODO: Delete-Sound
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")

                    # Fehler
                    else:
                        self._print(text, char, "Nicht gefunden!!")

                        # TODO: Error Sound
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")
                        # time.sleep(0.1)
                        # self.sound.beep(args="-l 100")


                    # Weiter warten
                    if not self.touch.wait_for_pressed(timeout_ms=(rest_long-rest_short)*1000):
                        # Leerzeichen
                        if len(text) > 0 and not text[-1] == " ":
                            text += " "
                            self._print(text, "", "Leerzeichen")

                            # TODO: Leerzeichen-Sound
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")
                            # time.sleep(0.1)
                            # self.sound.beep(args="-l 100")


                    # Nächster Charakter
                    break
