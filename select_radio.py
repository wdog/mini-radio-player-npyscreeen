#!/usr/bin/env python3

import npyscreen
from npyscreen import wgcheckbox  as checkbox

class RoundCheckBox(checkbox.Checkbox):
    
    False_box = ''
    True_box  = '»-»'

    def __init__(self, screen, value = False, **keywords):
        self.value = value
        super().__init__(screen, **keywords)


""" SELECT """
class SelectRadio(npyscreen.SelectOne):
    _contained_widgets = RoundCheckBox

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)

    def create(self):
        super().create()

    def h_select(self, ch):
        # update row selection
        self.value= [self.cursor_line,]
        # return radio selected by row
        self.parent.parentApp.activate_play(self.values[self.cursor_line])


