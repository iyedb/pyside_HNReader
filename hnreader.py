#!/usr/bin/env python

import sys,os
from PySide.QtGui import QApplication,QSystemTrayIcon, QIcon
from PySide.QtCore import QUrl, QSize
from mainwindow import MainWindow
		
#refactor 		
def _quit():
	app.quit()
	qDebug('bye!')
	
def show_window(thereason):
	if thereason == QSystemTrayIcon.ActivationReason.Trigger:
		if main_window.isVisible() == True:
			main_window.hide()
		main_window.show()

#create the QApplication instance before any other widget
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)	

ico = QIcon(os.path.join(os.getcwd(),'yhn.png'))
systrayico = QSystemTrayIcon(ico)
systrayico.activated.connect(show_window)
systrayico.show()

x_pos = systrayico.geometry().left()
y_pos = app.desktop().availableGeometry(app.desktop().primaryScreen()).topLeft().y()

main_window = MainWindow(x_pos, y_pos, 420, 500)

sys.exit(app.exec_())



	
