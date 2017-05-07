#!/usr/bin/python

import time
import json
from dotstar import Adafruit_DotStar


class AwkwardLights():
    brightness = 100
    fade = 1
    update = 30
    update_interval = 30
    light_interval = 1.0 / 50

    def __init__(self):
        self.update_data()
        self.strip = Adafruit_DotStar(len(self.people) * 2)
        self.strip.begin()
        self.loop()

    def loop(self):
        while True:
            for index, person in enumerate(self.people):
                left_eye_index = index * 2
                right_eye_index = left_eye_index + 1

                if person["in"] is True:
                    colour = int(person["eyes"], 16)
                else:
                    colour = 0

                self.strip.setPixelColor(left_eye_index, colour)
                self.strip.setPixelColor(right_eye_index, colour)

            self.check_update_interval()
            self.update_brightness()
            self.strip.setBrightness(self.brightness)
            self.strip.show()
            time.sleep(self.light_interval)

    def update_data(self):
        # set absolute path if running on pi load
        with open('people.json') as data_file:
            self.people = json.load(data_file)
            print self.people

    def update_brightness(self):
        self.brightness = self.brightness + self.fade
        if (self.brightness <= 1 or self.brightness > 100):
            self.fade = -self.fade

    def check_update_interval(self):
        self.update_interval = self.update_interval - self.light_interval
        if self.update_interval <= 0:
            self.update_data()
            self.update_interval = self.update


# init
awk_lights = AwkwardLights()
