#!/usr/bin/env python3

import npyscreen
import random
import logging
import sys
import json
from station import Station
import pprint

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.sm = Station()

        # Set the theme. DefaultTheme is used by default
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", MainForm, name="Mini-Radio-Player",draw_line_at=22)


class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.SplitForm):

    OK_BUTTON_TEXT='Quit'

    def create(self):
        y, x = self.useable_space()

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application
        #self.show_atx = (50-10)//2 
        #self.show_aty = 0
        self.stations = self.add(npyscreen.SelectOne,name='stations', value =
                [0,], max_height=18,  values= self.parentApp.sm.stations)
        self.info     = self.add(npyscreen.TitleText, name='Info:', value='', rely=-5)
        self.url      = self.add(npyscreen.TitleText, name='Url:', value='', rely=-4)
        self.current_station      = self.add(npyscreen.TitleText, name='Now On Air:', value='', rely=-3)
        

        self.menu = self.new_menu(name="Menu", shortcut='m')
        self.menu.addItem( "DEBUG", self.info, '^I')
        self.menu.addItem( "Quit", self.exit_application , '^X')

    def info(self):
        logging.debug(self.stations.get_selected_objects()[0].name)

    def event_value_edited(self, event):
        logging.debug(event)

    def exit_application(self):
        self.parentApp.switchForm(None)

    def adjust_widgets(self):
        logging.debug(self.stations.get_selected_objects()[0].name)
        self.current_station.value = self.stations.get_selected_objects()[0].name
        self.url.value = self.stations.get_selected_objects()[0].url
        self.current_station.update()
        self.url.update()


if __name__ == '__main__':
    logging.basicConfig(filename="app.log", format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S', level=logging.DEBUG)
    npyscreen.wrapper(App().run())
