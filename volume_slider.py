#!/usr/bin/env python3
import npyscreen


class VolumeSlider(npyscreen.Slider):

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)

    def create(self):
        super().create()

    def translate_value(self):
        return "Volume {:2d} %".format(int(self.value))
#

    def h_increase(self, ch):
        if (self.value + self.step <= self.out_of):
            self.value += self.step
            self.parent.parentApp.queue_event(npyscreen.Event("ev_set_volume"))

    def h_decrease(self, ch):
        if (self.value - self.step >= self.lowest):
            self.value -= self.step
            self.parent.parentApp.queue_event(npyscreen.Event("ev_set_volume"))
