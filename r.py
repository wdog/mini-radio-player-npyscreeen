#!/usr/bin/env python3

import npyscreen
import logging
from station import Station
from player import Player
from select_radio import SelectBoxRadio
from volume_slider import VolumeSlider
from color_theme import AppColorTheme
import time


class App(npyscreen.StandardApp):
    def onStart(self):
        # station manager
        self.sm = Station()
        self.player = Player()
        # Set the theme.
        npyscreen.setTheme(AppColorTheme)

        self.main = self.addForm("MAIN", MainForm, name="Mini-Radio-Player")
        self.order = self.addForm("ORDERFORM", OrderForm, name="Reorder Station")

    """ called when option is selected with enter or space """
    def activate_play(self, station):
        self.player.load_station((station))
        self.player.toggle()
        self.main.status_update()

class OrderForm(npyscreen.ActionForm):
    def create(self):
        y, x = self.useable_space()

        self.src = self.add(npyscreen.TitleSelectOne, name="Move Selected Radio:", relx= 1, rely=1, width=(x//2) - 5,
                                    scroll_exit=True, max_height=y - 3 , values = self.parentApp.sm.stations)

        self.dst = self.add(npyscreen.TitleSelectOne, name="Prepend Selected Position:", relx= (x // 2)+3, rely=1, width=(x//2) - 5,
                scroll_exit=True, max_height= y - 3 , values = self.parentApp.sm.stations)

    def beforeEditing(self):
        self.src.value=0
        self.dst.value=0
        self.update_list()
    
    def update_list(self):
        self.parentApp.sm.load_stations_list()
        self.src.values = self.parentApp.sm.stations
        self.src.display()
        self.dst.values = self.parentApp.sm.stations
        self.dst.display()

    def on_ok(self):
        self.parentApp.sm.change_order(self.src.value,self.dst.value)
        self.parentApp.sm.load_stations_list()
        self.show_main()

    def on_cancel(self):
        self.show_main()

    def show_main(self):
        self.parentApp.switchForm('MAIN')


class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.Form):

    def beforeEditing(self):
        self.update_list()
    
    def update_list(self):
        self.parentApp.sm.load_stations_list()
        self.stations.values = self.parentApp.sm.stations
        self.stations.display()

    def create(self):
        y, x = self.useable_space()

        self.stations = self.add(SelectBoxRadio, name='STATIONS', value=[0, ],
                                 rely = 1, 
                                 max_height=(y-8),
                                 values=self.parentApp.sm.stations,
                                 scroll_exit=False)

        self.status = {
            'status_info': self.add(npyscreen.TitleText, editable=False,
                                    name='Station:', value='',
                                    rely=-7, begin_entry_at=14),
            'status_url': self.add(npyscreen.TitleText, editable=False,
                                   name='Genere:', value='',
                                   rely=-6, begin_entry_at=14),
            'status_name': self.add(npyscreen.TitleText, editable=False,
                                    name='Now On Air:', value='',
                                    rely=-5, begin_entry_at=14),
        }
        self.volume = self.add(VolumeSlider, name="volume", out_of=100,
                               lowest=1, value=self.parentApp.player.volume,
                               step=5, rely=-3, label=True)

        """ MENU """
        self.menu = self.new_menu(name="Menu", shortcut='m')

        self.menu.addItemsFromList([
            ("HELP",None,''),
            ("---",None,''),
            ("m) Mute",None),
            ("x ENTER SPACEBAR) Play/Pause",None),
            ("l) Filter Station",None),
            (),
            ("Exit Application", self.exit_application, "^X")])

        """ HANDLERS """
        # update station info
        self.add_handlers({ord('i'): self.status_update})
        # quit q/Q
        self.add_handlers({
            ord('q'): self.exit_application,
            ord('Q'): self.exit_application, })
        # MUTE
        self.add_handlers({ord('m'):  self.toggle_mute})
        # REORDER RADIO
        self.add_handlers({ord('o'):  self.form_order})
        # QUIT ESC
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = \
            self.exit_application
        
        # on select station
        self.add_event_hander("ev_station_select", self.ev_station_select)
        # on change volume
        self.add_event_hander("ev_set_volume", self.ev_set_volume)




    def ev_station_select(self, event):
        self.parentApp.activate_play( self.stations.values[self.stations.value[0]])

    def ev_set_volume(self, event):
        self.parentApp.player.set_volume(self.volume.value)

    def status_update(self, ch=''):

        if not self.parentApp.player.is_playing:
            self.status['status_name'].value = ""
            self.status['status_url'].value = ""
            self.status['status_info'].value = "[-] PAUSE"
        else:
            self.info_station = self.parentApp.player.get_info()
            self.status['status_name'].value = self.info_station[2]
            self.status['status_url'].value = self.info_station[1]
            self.status['status_info'].value = self.info_station[0]

        self.status['status_name'].update()
        self.status['status_url'].update()
        self.status['status_info'].update()

    def toggle_mute(self, ch):
        self.parentApp.player.toggle_mute()

    """ quit app """
    def exit_application(self, ch=''):
        self.parentApp.switchForm(None)

    def form_order(self, *args, **keywords):
        self.parentApp.switchForm('ORDERFORM')
        

if __name__ == '__main__':
    logging.basicConfig(filename="app.log",
                        format='%(name)s [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    npyscreen.wrapper(App().run())
