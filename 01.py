#!/usr/bin/env python

import npyscreen

class FormObject(npyscreen.ActionForm):


    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "" )
        self.add(npyscreen.TitleText, name = "Text:", value= "" )
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add(npyscreen.FixedText, value=what_to_display)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False

    def afterEditing(self):
        self.parentApp.setNextForm(None)

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addFormClass('MAIN',FormObject, name='Mini RAdio Player')

        

if __name__ == '__main__':
    app = App()
    app.run()
