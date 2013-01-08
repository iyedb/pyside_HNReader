from PySide.QtCore import QThread, QUrl
from lxml import etree
from urllib2 import urlopen
from mako.template import Template



class HNhtmlGenerator(QThread):
	"""docstring for HNhtmlGenerator"""
	def __init__(self):
		super(HNhtmlGenerator, self).__init__()
		self.html = u''

	def run(self):
		self.html = self.generateHtml()

	def getHtml(self):
		return self.html

	def processSubtexttr(self,tr_tag):
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

	def generateHtml(self):
		
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
					d = self.processSubtexttr(tr_subtext)

				entry['timestamp'] = d['timestamp']

				if 'comments_url' in d:
					entry['comments_url']  = d['comments_url']
				if 'comments_count' in d:
					entry['comments_count']  = d['comments_count']

				entries.append(entry)

		template_file = QUrl.fromLocalFile('template.html')	
		template = Template( filename=template_file.path() )	
		return template.render_unicode(rows=entries)

		