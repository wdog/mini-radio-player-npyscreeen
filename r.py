#!/usr/bin/env python3

import npyscreen
import random
import logging
import sys
import json
from station import Station
from player import Player
import curses


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        # station manager
        self.sm = Station()
        self.player = Player()
        # Set the theme. DefaultTheme is used by default
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.main = self.addForm("MAIN", MainForm,
                name="Mini-Radio-Player",draw_line_at=20)

    def activate_play(self,station):
        logging.info('play')
        self.player.load_station((station))
        self.player.play()
        self.main.get_info()



class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.SplitForm):

    OK_BUTTON_TEXT='Quit'

    def create(self):
        y, x = self.useable_space()

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application
        #self.show_atx = (50-10)//2 
        #self.show_aty = 0
        self.stations = self.add(SelectRadio,
                container=11,
                name='stations', 
                value = [0,], 
                max_height=18,  
                values= self.parentApp.sm.stations,
                scroll_exit=False
                )


        self.status_info = self.add(npyscreen.TitleText, name='Info:', value='', rely=-5)
        self.status_url  = self.add(npyscreen.TitleText, name='Url:', value='', rely=-4)
        self.status_name = self.add(npyscreen.TitleText, name='Now On Air:', value='', rely=-3)
        
        self.menu = self.new_menu(name="Menu", shortcut='m')
        self.menu.addItem( "DEBUG", self.get_menu, '^I')
        self.menu.addItem( "Quit", self.exit_application , '^X')

        self.add_handlers({ 
            ord('q'): self.exit_application, 
            ord('Q'): self.exit_application, })

        self.add_handlers({ ord('m'): self.toggle})
        self.add_handlers({ ord('i'): self.get_info})

    def toggle(self,ch):
        self.parentApp.player.toggle()
        self.status_name.value = "paused"
        self.status_name.update()
        self.status_url.value = "" 
        self.status_url.update()
        self.status_info.value = ""
        self.status_info.update()
        self.get_info(ch)

    def get_menu(self):
        logging.debug(self.stations.get_selected_objects()[0].url)

    def get_info(self,ch=''):
        self.info_station = self.parentApp.player.get_info()
        self.status_name.value = self.info_station[2]
        self.status_name.update()
        self.status_url.value = self.info_station[1]
        self.status_url.update()
        self.status_info.value = self.info_station[0] 
        self.status_info.update()

    """ quit app """
    def exit_application(self,ch):
        self.parentApp.switchForm(None)

""" SELECT """
class SelectRadio(npyscreen.SelectOne):

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)

    def create(self):
        super().create()

    def h_select(self, ch):
        # update row selection
        self.value= [self.cursor_line,]
        # return radio selected by row
        self.parent.parentApp.activate_play(self.values[self.cursor_line])




if __name__ == '__main__':
    logging.basicConfig(filename="app.log", format='%(name)s [%(levelname)s] %(message)s',
                            datefmt='%H:%M:%S', level=logging.DEBUG)
    npyscreen.wrapper(App().run())
