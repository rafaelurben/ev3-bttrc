#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound

from multiprocessing import Process, Manager
import time


class Printer():
    _manager = Manager()

    queue = _manager.list()

    button = Button()
    sound = Sound()
    _led = Leds()

    penupdownmover = MediumMotor(OUTPUT_C)
    pensidemover = LargeMotor(OUTPUT_A)
    papermover = LargeMotor(OUTPUT_B)
    paperdetector = ColorSensor(INPUT_4)

    size = 10

    _tank = MoveTank(OUTPUT_A, OUTPUT_B)

    _line_width = 1050                # NICHT ÄNDERN
    _line_position = _line_width/2
    _pen_is_down = False
    _nowplaying = None

    @classmethod
    def _setState(self, state):
        setcolor = lambda color: self._led.set_color("RIGHT", color.upper())
        if state == "IDLE":
            setcolor("GREEN")

        elif state == "WAIT":
            setcolor("ORANGE")

        elif state == "WORK":
            setcolor("YELLOW")

        elif state == "ERROR":
            setcolor("RED")

    @classmethod
    def _stopsound(self):
        if self._nowplaying is not None:
            self._nowplaying.kill()

    @classmethod
    def _paper_is_in(self):
        return bool(self.paperdetector.reflected_light_intensity > 2)

    @classmethod
    def _pen_up(self):
        if self._pen_is_down:
            self.penupdownmover.on_for_rotations(SpeedPercent(25), 0.5, brake=True)
            self._pen_is_down = False


    @classmethod
    def _pen_down(self):
        if not self._pen_is_down and self._paper_is_in():
            self.penupdownmover.on_for_rotations(SpeedPercent(25), -0.5, brake=True)
            self._pen_is_down = True

    @classmethod
    def _feed_in(self):
        self._pen_up()
        self.papermover.on(SpeedPercent(-50), brake=False, block=False)
        while not self._paper_is_in():
            pass
        self.papermover.stop()
        self.papermover.on_for_degrees(SpeedPercent(50), 1)

    @classmethod
    def _feed_out(self):
        self._pen_up()
        self._carriage_move(self._line_width/2)
        self.papermover.on(SpeedPercent(50), brake=False, block=False)
        while self._paper_is_in():
            pass
        self.papermover.stop()
        self.papermover.on_for_degrees(SpeedPercent(50), 720)

    @classmethod
    def _line_feed(self):
        self._pen_up()
        self.papermover.on_for_degrees(SpeedPercent(-20), (self.size*4))
        self.papermover.on_for_degrees(SpeedPercent(-20), 20)

    @classmethod
    def _carriage_move(self, position=0):
        self._pen_up()
        self.pensidemover.on_for_degrees(SpeedPercent(50), position-self._line_position)
        if position == 0:
            self.pensidemover.on_for_degrees(SpeedPercent(50), -20)
        self._line_position = position

    @classmethod
    def _carriage_return(self):
        self._carriage_move(0)
        self._line_feed()

    @classmethod
    def _print_letter(self, letter):
        self._setState("WORK")
        self._pen_up()

        letter = letter.upper()
        seg1 = self.size*1
        seg2 = self.size*2
        seg3 = self.size*3
        seg4 = self.size*4

        pos = SpeedPercent(20)
        pos_slow = SpeedPercent(10)
        neg = SpeedPercent(-20)
        neg_slow = SpeedPercent(-10)

        move_a = self.pensidemover.on_for_degrees
        move_b = self.papermover.on_for_degrees
        move_tank = self._tank.on_for_degrees

        pen_up = self._pen_up
        pen_down = self._pen_down

        letterwidth = seg4

        print("[Printer] - Drucken: "+str(letter))

        if letter in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]:
            if letter == "A":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                move_a(pos, seg4)
                move_b(neg, seg4)
                move_b(pos, seg2)
                move_a(neg, seg4)
                pen_up()
                move_a(pos, seg4)
                move_b(pos, seg2)
            elif letter == "B":
                pen_down()
                move_b(neg, seg4)
                move_a(pos, seg3)
                move_tank(pos, pos, seg1)
                move_tank(neg, pos, seg1)
                move_a(neg, seg3)
                move_a(pos, seg3)
                move_tank(pos, pos, seg1)
                move_tank(neg, pos, seg1)
                move_a(neg, seg3)
                pen_up()
                move_a(pos, seg4)
            elif letter == "C":
                move_a(pos, seg4)
                move_a(neg, 10)
                move_b(neg, seg4)
                pen_down()
                move_a(neg, seg4)
                move_b(pos, seg4)
                move_a(pos, seg4)
                pen_up()
                move_a(pos, 10)
            elif letter == "D":
                pen_down()
                move_b(neg, seg4)
                move_a(pos, seg2)
                move_tank(pos_slow, pos_slow, seg2)
                move_tank(neg_slow, pos_slow, seg2)
                move_a(neg, seg2)
                pen_up()
                move_a(pos, seg4)
            elif letter == "E":
                move_a(pos, seg4)
                move_a(pos, -10)
                move_b(neg, seg4)
                pen_down()
                move_a(neg, seg4)
                move_b(pos, seg2)
                move_a(pos, seg3)
                move_a(neg, seg3)
                move_b(pos, seg2)
                move_a(pos, seg4)
                pen_up()
                move_a(pos, 10)
            elif letter == "F":
                move_a(pos, seg4)
                move_a(pos, -10)
                pen_down()
                move_a(neg, seg4)
                move_b(neg, seg2)
                move_a(pos, seg3)
                move_a(neg, seg3)
                move_b(neg, seg2)
                pen_up()
                move_a(pos, 10)
                move_a(pos, seg4)
                move_b(pos, seg4)
            elif letter == "G":
                move_b(neg, seg1)
                move_a(pos, seg4)
                move_a(pos, -10)
                pen_down()
                move_tank(neg_slow, pos_slow, seg1)
                move_a(neg, seg2)
                move_tank(neg_slow, neg_slow, seg1)
                move_b(neg, seg2)
                move_tank(pos_slow, neg_slow, seg1)
                move_a(pos, seg2)
                move_tank(pos_slow, pos_slow, seg1)
                move_b(neg, seg1)
                move_b(pos, seg2)
                move_a(neg, seg2)
                pen_up()
                move_b(pos, seg2)
                move_a(pos, seg2)
                move_a(pos, 10)
            elif letter == "H":
                pen_down()
                move_b(neg, seg4)
                move_b(pos, seg2)
                move_a(pos, seg4)
                move_b(neg, seg2)
                move_b(pos, seg4)
                pen_up()
            elif letter == "I":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                pen_up()
                letterwidth = 0
            elif letter == "J":
                move_a(pos, seg4)
                move_a(neg, 10)
                pen_down()
                move_b(neg, seg3)
                move_tank(neg_slow, neg_slow, seg1)
                move_a(neg_slow, seg2)
                move_tank(neg_slow, pos_slow, seg1)
                move_b(pos, seg1)
                pen_up()
                move_b(pos, seg2)
                move_a(pos, seg4)
                move_a(pos, 10)
            elif letter == "K":
                pen_down()
                move_b(neg, seg4)
                move_b(pos, seg2)
                move_tank(pos, pos_slow, seg4)
                time.sleep(0.1)
                move_tank(neg, neg_slow, seg4)
                move_tank(pos, neg_slow, seg4)
                pen_up()
                move_b(pos, seg4)
            elif letter == "L":
                pen_down()
                move_b(neg, seg4)
                move_a(pos, seg4)
                pen_up()
                move_b(pos, seg4)
            elif letter == "M":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                move_tank(pos_slow, neg_slow, seg2)
                time.sleep(0.05)
                move_tank(pos_slow, pos_slow, seg2)
                move_b(neg, seg4)
                pen_up()
                move_b(pos, seg4)
            elif letter == "N":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                move_tank(pos, neg, seg4)
                move_b(pos, seg4)
                pen_up()
            elif letter == "O":
                move_b(neg, seg1)
                pen_down()
                move_b(neg, seg2)
                move_tank(pos_slow, neg_slow, seg1)
                move_a(pos, seg2)
                move_tank(pos_slow, pos_slow, seg1)
                move_b(pos, seg2)
                move_tank(neg_slow, pos_slow, seg1)
                move_a(neg, seg2)
                move_tank(neg_slow, neg_slow, seg1)
                pen_up()
                move_b(pos, seg1)
                move_a(pos, seg4)
            elif letter == "P":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                move_a(pos, seg4)
                move_b(neg, seg2)
                move_a(neg, seg4)
                pen_up()
                move_a(pos, seg4)
                move_b(pos, seg2)
            elif letter == "Q":
                move_b(neg, seg1)
                pen_down()
                move_b(neg, seg2)
                move_tank(pos_slow, neg_slow, seg1)
                move_a(pos, seg2)
                move_tank(pos_slow, pos_slow, seg1)
                move_b(pos, seg2)
                move_tank(neg_slow, pos_slow, seg1)
                move_a(neg, seg2)
                move_tank(neg_slow, neg_slow, seg1)
                pen_up()
                move_b(neg, seg1)
                move_a(pos, seg2)
                pen_down()
                move_tank(pos, neg, seg2)
                pen_up()
                move_b(pos, seg4)
            elif letter == "R":
                move_b(neg, seg4)
                pen_down()
                move_b(pos, seg4)
                move_a(pos, seg3)
                move_tank(pos_slow, neg_slow, seg1)
                move_tank(neg_slow, neg_slow, seg1)
                move_a(neg, seg3)
                move_a(pos, seg2)
                move_tank(pos_slow, neg_slow, seg2)
                pen_up()
                move_b(pos, seg4)
            elif letter == "S":
                move_a(pos, seg4)
                pen_down()
                move_a(neg, seg4)
                move_b(neg, seg2)
                move_a(pos, seg4)
                move_b(neg, seg2)
                move_a(neg, seg4)
                pen_up()
                move_a(pos, seg4)
                move_b(pos, seg4)
            elif letter == "T":
                pen_down()
                move_a(pos, seg4)
                move_a(neg, seg3)
                move_b(neg, seg4)
                pen_up()
                move_b(pos, seg4)
                move_a(pos, seg3)
            elif letter == "U":
                pen_down()
                move_b(neg, seg4)
                move_a(pos, seg4)
                move_b(pos, seg4)
                pen_up()
            elif letter == "V":
                pen_down()
                move_tank(pos_slow, neg, seg4)
                move_tank(pos_slow, pos, seg4)
                pen_up()
            elif letter == "W":
                pen_down()
                move_b(neg, seg4)
                move_tank(pos_slow, pos_slow, seg2)
                move_tank(pos_slow, neg_slow, seg2)
                move_b(pos, seg4)
                pen_up()
            elif letter == "X":
                pen_down()
                move_tank(pos, neg, seg4)
                pen_up()
                move_a(neg, seg4)
                pen_down()
                move_tank(pos, pos, seg4)
                pen_up()
            elif letter == "Y":
                pen_down()
                move_tank(pos, neg, seg2)
                move_b(neg, seg2)
                move_b(pos, seg2)
                move_tank(pos, pos, seg2)
                pen_up()
            elif letter == "Z":
                pen_down()
                move_a(pos, seg4)
                move_tank(neg, neg, seg4)
                move_a(pos, seg4)
                pen_up()
                move_b(pos, seg4)
            elif letter == " ":
                move_a(pos, seg4)

            move_a(pos, seg1) # letter spacing
            self._line_position = (self._line_position + letterwidth + seg1)

        elif letter.startswith("//") and letter.endswith("//"):
            command = letter.strip("/")
            if command in ["NEWLINE"]:
                self._carriage_return()
            elif command in ["FEEDOUT"]:
                self._feed_out()
            elif command.startswith("SOUND:"):
                self._stopsound()
                filename = command[6::].lower()
                try:
                    self._nowplaying = self.sound.play_file("/home/robot/ev3-bttrc/files/"+str(filename)+".wav", play_type=1)
                except ValueError:
                    print("[Printer] - Tondatei nicht gefunden: "+str(filename)+".wav")
            elif command in ["STOPSOUND"]:
                self._stopsound()
            else:
                print("[Printer] - Unbekannter Befehl: "+str(command))
        else:
            print("[Printer] - Unbekannter Buchstabe: "+str(letter))

        if self._line_position >= self._line_width:
            self._carriage_return()
        self._setState("IDLE")

    @classmethod
    def _print_next(self):
        self._print_letter(self.queue.pop(0))

    @classmethod
    def _move_left_and_right(self):
        while True:
            self._carriage_move(0)
            time.sleep(0.25)
            self._carriage_move(self._line_width)
            time.sleep(0.25)

    @classmethod
    def _reset_motors(self, resetheight=False):
        self.pensidemover.on_for_degrees(SpeedPercent(50), -(self._line_width+100))
        self.pensidemover.reset()
        self._line_position = 0
        if resetheight:
            self.penupdownmover.reset()
            self._pen_is_down = True


    @classmethod
    def calibrate(self):
        if not self._paper_is_in():
            self._setState("WAIT")
            self._feed_in()

        self._setState("WORK")

        print("[Printer] - Kalibrierung: Starten...")
        self.penupdownmover.on_for_rotations(SpeedPercent(20), -2.5)

        time.sleep(2)

        moveprocess = Process(target=self._move_left_and_right)
        moveprocess.start()

        self._setState("IDLE")

        print("[Printer] - Kalibrierung: Gestartet!")
        while True:
            if self.button.up:
                print("[Printer] - Kalibrierung: Nach oben!")
                self.penupdownmover.on_for_degrees(SpeedPercent(25), 5)
            elif self.button.down:
                print("[Printer] - Kalibrierung: Nach unten!")
                self.penupdownmover.on_for_degrees(SpeedPercent(-25), 5)
            elif self.button.enter:
                break
        print("[Printer] - Kalibrierung: Beenden...")

        self._setState("WORK")

        moveprocess.terminate()

        time.sleep(0.5)
        self._reset_motors(resetheight=True)
        time.sleep(2)
        self._pen_up()
        self._carriage_move(self._line_width/2)

        self._led.all_off()
        print("[Printer] - Kalibrierung: Beendet...")
        return
        
    @classmethod
    def addToQueue(self, string:str):
        string = string.strip().upper().replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
        command = ""
        for letter in string:
            if (command != "") or letter == "/":
                command += letter
                if command.startswith("//") and command.endswith("//") and len(command) > 2:
                    self.queue.append(command)
                    #print("[Printer] - Befehl zur Warteschlange hinzugefuegt: '"+command+"'")
                    command = ""
                elif len(command) == 2 and not command == "//":
                    for letter in command:
                        self.queue.append(letter)
                        #print("[Printer] - Zur Warteschlange hinzugefuegt: '"+letter+"'")
                    command = ""
            else:
                self.queue.append(letter)
                #print("[Printer] - Zur Warteschlange hinzugefuegt: '"+letter+"'")

    @classmethod
    def printQueue(self, queue):
        time.sleep(0.5)
        for letter in queue:
            self._print_letter(letter)

    @classmethod
    def processQueue(self):
        self._reset_motors()
        while True:
            self._setState("IDLE")
            if self._paper_is_in():
                if bool(self.button.down):
                    self._setState("WORK")
                    print("[Printer] - Papier wird ausgegeben...")
                    self._feed_out()
                elif bool(self.button.up):
                    self._setState("WORK")
                    print("[Printer] - Neue Zeile...")
                    self._carriage_return()
                elif bool(self.button.right):
                    print("[Printer] - Audio stoppen...")
                    self._stopsound()
                elif self.queue[:] != []:
                    self._print_next()
                else:
                    time.sleep(0.25)
            else:
                self._setState("WAIT")
                print("[Printer] - Druecke die UP Taste!")
                self.button.wait_for_bump(["up"])
                self._feed_in()
                self._carriage_move(0)
                self._setState("IDLE")
                print("[Printer] - Bereit zum Drucken!")
