__author__ = 'Johannes'
from lib.camera import Camera
from helpers import Helpers as h
import time


class SearchRed(object):

    def __init__(self, BBC, max_pri):
        self.BBC = BBC
        self.camera = Camera()
        self.image = None
        self.speed = 0.2
        self.weight = 0
        self.weight_thr = 10
        self.recommendation = None
        self.max_pri = max_pri
        self.last_update = 0

    def update_sensor(self):
        self.image = self.camera.update()
        self.weight, pos = h.get_red(self.image)
        if pos < 0:
            self.recommendation = [-self.speed, self.speed - (pos / 2)]
        elif pos > 0:
            self.recommendation = [self.speed + (pos/2), -self.speed]
        else:
            self.recommendation = [self.speed, self.speed]

    def update(self):
        self.weight = 0
        now = self.BBC.current_time_millis()
        if now - self.last_update > 2000:
            self.update_sensor()
            if self.weight > self.weight_thr:
                self.BBC.activate_behavior(self)
            else:
                self.BBC.deactivate_behavior(self)
            self.last_update = self.BBC.current_time_millis()

    def get_weight(self):
        print("W: " + str(self.weight))
        return self.weight

    def get_motor_recommendation(self):
        print("R: " + str(self.recommendation))
        return self.recommendation, 0.4

