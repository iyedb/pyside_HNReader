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
		#if url = QUrl('about:blank#quit'):
		#QApplication.instance().quit()
		QDesktopServices.openUrl(url)

	def th_started(self):
		pass

	def th_finished(self):
		self.view.setHtml( self.th.getHtml() )

	def showEvent(self, event):
		self.th.start()

	"""
	def generate_html(self):

		def process_subtexttr(tr_tag):
			strings = []
			for i in tr_tag.itertext():
				strings.append(i.decode('utf-8'))

			entry = dict()
		  	if len(strings) == 5:
				entry['timestamp'] = strings[-2].strip(' |')
			else:
				entry['timestamp'] = strings[-1].strip()

			anchors = tr_tag.xpath('td/a')
			if len(anchors) == 2:
				entry['comments_count'] = anchors[-1].text.decode('utf-8')
				entry['comments_url'] = anchors[-1].get('href').decode('utf-8')
			return entry
		
		doc = urlopen('http://news.ycombinator.com/')
		unicode_string = doc.read().decode('utf-8')
		e = etree.fromstring(unicode_string, etree.HTMLParser())

		entries = []

		for i in e.xpath('//td/a'):
			if len(i.getparent().keys()) == 1 and i.getparent().values()[0] == 'title':
				if isinstance(i.text, str):
					u_s = i.text.decode('utf-8')
				else:
					u_s = i.text

				if u_s == u'More':
					continue

				entry = dict()

				entry['site'] = u''
				entry['comments_url'] = u''
				entry['comments_count'] = u''		    
				entry['story_link'] = u_s
				entry['story_url'] = i.get('href').decode('utf-8')

				span_tag = i.getnext() #may be None if 'Ask HN'
				if not span_tag is None:
					entry['site'] = span_tag.text.decode('utf-8').strip()		     

				tr_subtext = i.getparent().getparent().getnext()

				if not tr_subtext is None:
					d = process_subtexttr(tr_subtext)

				entry['timestamp'] = d['timestamp']

				if 'comments_url' in d:
					entry['comments_url']  = d['comments_url']
				if 'comments_count' in d:
					entry['comments_count']  = d['comments_count']

				entries.append(entry)

		template_file = QUrl.fromLocalFile('template.html')	
		template = Template( filename=template_file.path() )	
		return template.render_unicode(rows=entries)
	"""




