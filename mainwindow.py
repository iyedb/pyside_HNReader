from PySide.QtCore import Qt, QUrl, QSize
from PySide.QtGui import QApplication, QMainWindow, QApplication, QDesktopServices
from PySide.QtWebKit import QWebView, QWebPage
from lxml import etree
from urllib2 import urlopen
from mako.template import Template
from htmlgenerator import HNhtmlGenerator


class MainWindow(QMainWindow):
	def __init__(self, x_pox, y_pos, width, height):
		super(MainWindow, self).__init__()

		self.setGeometry(x_pox, y_pos, width, height)
		self.setMaximumSize(width, height)
		self.setMinimumSize(width, height)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.setWindowFlags(self.windowFlags() | Qt.Tool)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

		self.view = QWebView(self)
		self.view.page().setViewportSize(QSize(width, height))
		self.view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
		self.view.page().linkClicked.connect(self.link_click_handler)

		self.th = HNhtmlGenerator()
		self.th.started.connect(self.th_started)
		self.th.finished.connect(self.th_finished)

		super(MainWindow, self).setCentralWidget(self.view)
	
	def link_click_handler(self, url):
		if url.path() == u'blank':
			if url.hasFragment():
				if url.fragment() == u'quit':
					QApplication.instance().quit()
		else:			
			QDesktopServices.openUrl(url)

	def th_started(self):
		pass

	def th_finished(self):
		self.view.setHtml( self.th.getHtml() )

	def showEvent(self, event):
		self.th.start()




