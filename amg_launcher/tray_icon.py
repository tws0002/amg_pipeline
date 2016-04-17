from PySide.QtCore import *
from PySide.QtGui import *
import os, sys, tempfile
from icons import icons
import cmd_listener

tray_message_title = 'AMG Pipeline'

class TrayIconClass(QSystemTrayIcon):
    def __init__(self):
        super(TrayIconClass, self).__init__()
        self.setIcon(QIcon(icons['animagrad']))
        self.activated.connect(self.tray_icon_activated)
        self.listener = cmd_listener.AMGListener()
        self.listener.messageSignal.connect(self.tray_message)
        self.show()

    @Slot()
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            print 'CONFIG MENU'
            self.tray_message('CONFIG MENU')
        elif reason == QSystemTrayIcon.Trigger:
            print 'MAIN WINDOW'
            self.tray_message('MAIN WINDOW')

    def tray_message(self, msg):
        self.showMessage(tray_message_title, msg)

    def exitEvent(self):
        self.exitOnClose = True
        self.hide()
        self.deleteLater()
        sys.exit()

    def show_help(self):
        self.tray_message('HELP!!!!!!!!!!!')

    def open_folder(self, path):
        import webbrowser
        webbrowser.open(path)


class customMenuStyle(QPlastiqueStyle):
    def __init__(self):
        super(customMenuStyle, self).__init__()

    def pixelMetric (self, metric, option,widget):
        if metric == QStyle.PM_SmallIconSize:
            return 22
        else:
            return super(customMenuStyle, self).pixelMetric(metric, option, widget)


if __name__ == '__main__':
    app = QApplication([])
    w = TrayIconClass()
    w.show()
    app.exec_()