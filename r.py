#!/usr/bin/env python3

import npyscreen
import random
import logging
import sys
import json
from station import Station
from player import Player
from select_radio import SelectRadio
from volume_slider import VolumeSlider
from color_theme import AppColorTheme
import curses


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        # station manager
        self.sm = Station()
        self.player = Player()
        # Set the theme. 
        npyscreen.setTheme(AppColorTheme)

        self.main = self.addForm("MAIN", MainForm, name="Mini-Radio-Player")

    """ called when option is selected with enter or space """
    def activate_play(self,station):
        self.player.load_station((station))
        self.player.toggle()
        self.main.status_update()



class MainForm(npyscreen.FormBaseNewWithMenus):

    OK_BUTTON_TEXT='Quit'

    def create(self):
        y, x = self.useable_space()

        self.stations = self.add(SelectRadio,
                name='stations', 
                value = [0,], 
                max_height=(y-9),  
                values= self.parentApp.sm.stations,
                scroll_exit=False
                )


        self.status_info = self.add(npyscreen.TitleText, editable=False, name='Station:', value='', rely=-6, begin_entry_at = 14)
        self.status_url  = self.add(npyscreen.TitleText, editable=False, name='Genere:', value='', rely=-5,begin_entry_at=14)
        self.status_name = self.add(npyscreen.TitleText, editable=False, name='Now On Air:', value='', rely=-4,begin_entry_at=14)

        self.add(VolumeSlider, 
                name="volume", 
                out_of=100, 
                lowest=1, 
                value=self.parentApp.player.volume,
                step=5, 
                rely= -3, 
                label=True,
                )

        """ MENU """
        self.menu = self.new_menu(name="Menu", shortcut='m')
        self.menu.addItem( "DEBUG", self.get_menu, '^I')
        self.menu.addItem( "Quit", self.exit_application , '^X')

        """ HANDLERS """
        # update station info
        self.add_handlers({ ord('i'): self.status_update})
        # quit q/Q
        self.add_handlers({ 
            ord('q'): self.exit_application, 
            ord('Q'): self.exit_application, })
        # quit ESC
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application

    def status_update(self,ch=''):

        if not self.parentApp.player.is_playing:
            self.status_name.value = "paused"
            self.status_url.value = "" 
            self.status_info.value = ""
        else: 
            self.info_station = self.parentApp.player.get_info()
            self.status_name.value = self.info_station[2]
            self.status_url.value = self.info_station[1]
            self.status_info.value = self.info_station[0] 

        self.status_name.update()
        self.status_url.update()
        self.status_info.update()

    def get_menu(self):
        logging.debug(self.stations.get_selected_objects()[0].url)

    """ quit app """
    def exit_application(self,ch=''):
        self.parentApp.switchForm(None)


if __name__ == '__main__':
    logging.basicConfig(filename="app.log", format='%(name)s [%(levelname)s] %(message)s',
                            datefmt='%H:%M:%S', level=logging.DEBUG)
    npyscreen.wrapper(App().run())
