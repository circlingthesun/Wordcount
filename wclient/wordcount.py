#!/usr/bin/python

import sys, os, time, subprocess
import signal
import settings, main
import ConfigParser
import threading
import urllib
from PySide.QtCore import *
from PySide.QtGui import *
from docxcount import countdocx
from latexcount import latexcount

signal.signal(signal.SIGINT, signal.SIG_DFL)

app_settings = {'document': "~", "group_id": "test_id", "username": "rickert", "password":"lala", "server_url": ""}
wordcount = 0
interval = 20
running = True
file_type = None

class Settings(QDialog):

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        
        self.settings = settings.Ui_Dialog()
        self.settings.setupUi(self)
        self.settings.open_button.clicked.connect(self.opendoc)

        self.settings.document.setText(app_settings["document"])
        self.settings.group_id.setText(app_settings["group_id"])
        self.settings.username.setText(app_settings["username"])
        self.settings.password.setText(app_settings["password"])

        self.show()


    def opendoc(self):
        fileName = QFileDialog.getOpenFileName(self, "Document", "~", "Documents (*.tex *.docx)")
        self.settings.document.setText(fileName[0])

    def accept(self):
        app_settings["document"] = self.settings.document.text()
        app_settings["group_id"] = self.settings.group_id.text()
        app_settings["username"] = self.settings.username.text()
        app_settings["password"] = self.settings.password.text()
        self.hide()

    def reject(self):
        self.hide()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainwindow = main.Ui_Form()
        self.mainwindow.setupUi(self)
        self.mainwindow.settings_button.clicked.connect(self.settings)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)


    def settings(self):
        settings = Settings(self)


class Counter(threading.Thread):
    def run(self):
        while True:
            global wordcount

            file_type = app_settings["document"].split(".")[-1]

            try:
                if file_type == "docx":
                    wordcount = countdocx(app_settings["document"])

                if file_type == "tex":
                    wordcount = latexcount(app_settings["document"])

            except Exception as e:
                print "Count failed:"
                print e

            main.mainwindow.wordcount.setText(str(wordcount))

            print wordcount
            print file_type

            params = urllib.urlencode({'c': str(wordcount), 'name': app_settings["username"]})


            try:
                f = urllib.urlopen(app_settings["server_url"], params)
                print f.read()
            except Exception as e:
                print "Cannot comunicate with server"
                print e

            time.sleep(interval)

 
if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    sfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
    config.read(sfile)

    app_settings["document"] = config.get('client', 'document')
    app_settings["group_id"] = config.get('client', 'group_id')
    app_settings["username"] = config.get('client', 'username')
    app_settings["password"] = config.get('client', 'password')
    app_settings["server_url"] = config.get('client', 'server_url')

    # Create the Qt Application
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    counter = Counter()
    counter.daemon = True;
    counter.start()

    # Run the main Qt loop
    status = app.exec_()

    # save config
    config.set('client', 'document', app_settings["document"])
    config.set('client', 'group_id', app_settings["group_id"])
    config.set('client', 'username', app_settings["username"])
    config.set('client', 'password', app_settings["password"])
    config.set('client', 'server_url', app_settings["server_url"])

    with open(sfile, 'wb') as configfile:
        config.write(configfile)

    sys.exit(status)