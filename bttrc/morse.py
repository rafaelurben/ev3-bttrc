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

def _beepWhileTouched(touchsensor, sound, press_long):
    while True:
        touchsensor.wait_for_pressed()
        p = sound.beep(args="-l "+str(int(press_long)*1000), play_type=1)
        touchsensor.wait_for_released()
        try:
            p.kill()
        except Exception as e:
            print("Error while beeping: ",e)

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
        print("Text: '"+text+"' Char: '"+char+"' Message: '"+message+"'")


    @classmethod
    def enterText(self, press_short=0.25, press_long=1, rest_short=1, rest_long=3):
        beepprocess = Process(target=_beepWhileTouched, args=(self.touch, self.sound, press_long))
        beepprocess.start()

        self._print("","","Warte auf Code...")
        self.display.text_grid(text="Warte auf Code...", x=0, y=0,  font="luBS14", clear_screen=True)
        self.display.update()

        text = ""
        while True:
            char = ""
            self.touch.wait_for_pressed(sleep_ms=0)
            while True:
                presstime_start = time.time()
                self.touch.wait_for_released(timeout_ms=press_long*1000, sleep_ms=0)
                presstime = 0-(presstime_start - time.time())

                # Kurz (Punkt)
                if presstime < press_short:
                    char += "."
                    #self.sound.beep(args="-l 50", play_type=1)
                    self._print(text, char, "Kurz!")

                # Lang (Strich)
                elif presstime >= press_short and presstime < press_long:
                    char += "-"
                    #self.sound.beep(args="-l 150", play_type=1)
                    self._print(text, char, "Lang!")

                # Gedrückt halten (Charakter zurücksetzen)
                else:
                    if not char == "":
                        self._print(text, "", "Abbruch!")

                        # TODO: Cancel-Sound
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")

                        self.touch.wait_for_released(sleep_ms=0)
                    break



                resttime_start = time.time()
                self.touch.wait_for_pressed(timeout_ms=rest_short*1000, sleep_ms=0)
                resttime = 0-(resttime_start - time.time())

                # Kurze Pause
                if resttime < rest_short:
                    pass

                # Lange Pause
                elif resttime >= rest_short:
                    # Charakter hinzufügen
                    if char in self.morse_alphabet_inverted:
                        text += self.morse_alphabet_inverted[char]
                        self._print(text, "", "Gefunden: "+self.morse_alphabet_inverted[char])

                        # TODO: Char-Sound
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")

                    # Ende der Nachricht / Ende der Übertragung
                    elif char == ".-.-." or char == "...-.-":
                        self._print(text, "", "Nachricht beendet!")

                        # TODO: Ende-Sound
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")

                        beepprocess.kill()
                        return str(text)

                    # Letztes Wort entfernen
                    elif char == "........":
                        text = text.rstrip()
                        while len(text) > 0 and text[-1] != " ":
                            text = text[:-1]
                        self._print(text, "", "Wort geloescht!")

                        # TODO: Delete-Sound
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")

                    # Fehler
                    else:
                        self._print(text, char, "Nicht gefunden!!")

                        # TODO: Error Sound
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")
                        time.sleep(0.1)
                        self.sound.beep(args="-l 100")


                    # Weiter warten, falls immer noch nicht gedrückt
                    if self.touch.is_released:
                        resttime_start = time.time()
                        self.touch.wait_for_pressed(timeout_ms=(rest_long-rest_short)*1000, sleep_ms=0)
                        resttime = 0-(resttime_start - time.time())

                        # Leerzeichen, wenn Timeout erreicht
                        if resttime > (rest_long-rest_short):
                            if len(text) > 0 and not text[-1] == " ":
                                text += " "
                                self._print(text, "", "Leerzeichen")

                                # TODO: Leerzeichen-Sound
                                self.sound.beep(args="-l 100")
                                time.sleep(0.1)
                                self.sound.beep(args="-l 100")
                                time.sleep(0.1)
                                self.sound.beep(args="-l 100")


                    # Nächster Charakter
                    break
