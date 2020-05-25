#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button

import time

class Printer():
    queue = []
    penupdownmover = MediumMotor(OUTPUT_C)
    pensidemover = LargeMotor(OUTPUT_A)
    papermover = LargeMotor(OUTPUT_B)
    paperdetector = ColorSensor(INPUT_4)

    letter_spacing = 20
    size = 10

    _tank = MoveTank(OUTPUT_A, OUTPUT_B)

    _line_width = 1050                # NICHT ÄNDERN

    _line_position = 0

    _pen_is_down = False
    _paper_is_in = False

    _interrupt_processing_queue = False

    @classmethod
    def _pen_up(self):
        if self._pen_is_down:
            self.penupdownmover.on_for_degrees(SpeedPercent(25), 180, break=True)
            self._pen_is_down = False

    @classmethod
    def _pen_down(self):
        if not self._pen_is_down and self._paper_is_in:
            self.penupdownmover.on_for_degrees(SpeedPercent(25), -180, break=True)
            self._pen_is_down = True

    @classmethod
    def _feed_in(self):
        self._pen_up()
        self.papermover.stop_action = "hold"
        while self.paperdetector.reflected_light_intensity < 50:
            self.papermover.on(SpeedPercent(-50), break=False, block=False)
        self.papermover.stop()
        self._paper_is_in = True

    @classmethod
    def _feed_out(self):
        self._pen_up()
        self._carriage_move(0)
        self.papermover.stop_action = "hold"
        while self.paperdetector.reflected_light_intensity > 50:
            self.papermover.on(SpeedPercent(50), break=False, block=False)
        self.papermover.stop()
        self.papermover.on_for_degrees(SpeedPercent(50), 600)
        self._paper_is_in = False

    @classmethod
    def _line_feed(self):
        self._pen_up()
        self.papermover.on_for_degrees(SpeedPercent(-20), (self.size*4))
        self.papermover.on_for_degrees(SpeedPercent(-20), 20)

    @classmethod
    def _carriage_move(self, position):
        self._pen_up()
        self.pensidemover.on_for_degrees(SpeedPercent(50), position-self._line_position)
        if position == 0:
            self.pensidemover.on_for_degrees(SpeedPercent(-20), 10)
            self.pensidemover.on_for_degrees(SpeedPercent(20), 10)
        self._line_position = position

    @classmethod
    def _carriage_return(self):
        self._carriage_move(0)
        self._line_feed()

    @classmethod():
    def _print_letter(self, letter):
        self._pen_up()

        letter = letter.upper()
        seg1 = self.size*1
        seg2 = self.size*2
        seg3 = self.size*3
        seg4 = self.size*4

        pos = SpeedPercent(20)
        neg = SpeedPercent(-20)

        move_a = self.pensidemover.on_for_degrees
        move_b = self.papermover.on_for_degrees
        move_tank = self._tank.on_for_degrees

        pen_up = self._pen_up
        pen_down = self._pen_down

        letterwidth = seg4

        print(letter)

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
                pass
            elif letter == "E":
                pass
            elif letter == "F":
                pass
            elif letter == "G":
                pass
            elif letter == "H":
                pass
            elif letter == "I":
                pass
            elif letter == "J":
                pass
            elif letter == "K":
                pass
            elif letter == "L":
                pass
            elif letter == "M":
                pass
            elif letter == "N":
                pass
            elif letter == "O":
                pass
            elif letter == "P":
                pass
            elif letter == "Q":
                pass
            elif letter == "R":
                pass
            elif letter == "S":
                pass
            elif letter == "T":
                pass
            elif letter == "U":
                pass
            elif letter == "V":
                pass
            elif letter == "W":
                pass
            elif letter == "X":
                pass
            elif letter == "Y":
                pass
            elif letter == "Z":
                pass

            elif letter == " ":
                self._carriage_move(self._line_position+seg4)

            move_a(pos, self.letter_spacing)
            self.carriage_move(self._line_position + letterwidth + self.letter_spacing)

        elif letter == "\n":
            self._carriage_return()
        elif letter == "//FEEDOUT//":
            self._feed_out()
        else:
            print("Unbekannter Buchstabe/Befehl!")

        if self._line_position >= self._line_width:
            self._carriage_return()


    @classmethod
    def addToQueue(self, string:str):
        if string in ["\n","//FEEDOUT//"]:
            self.queue.append(string)
        else:
            for s in string.upper():
                self.queue.append(s)

    @classmethod
    def printQueue(self, queue):
        self._interrupt_processing_queue = True
        time.sleep(0.5)
        for letter in queue:
            self._print_letter(letter)
        self._interrupt_processing_queue = False

    @classmethod
    def processQueue(self):
        while True:
            if self._paper_is_in:
                if not self._interrupt_processing_queue:
                    if self.queue != []:
                        self._print_letter(self.queue.pop(0))
                    elif Button.down:
                        self._feed_out()
                    else:
                        time.sleep(0.25)
                else:
                    time.sleep(0.25)
            else:
                print("Drücke die obere Taste, um das Papier einzuziehen.")
                Button.wait_for_bump(["up"])
                self._feed_in()
