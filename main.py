#!/usr/bin/python2.7
import sys

class RSSTorrent(object):
	def __init__(self, title, link):
		self.__title = title
		self.__link = link

	def _getTitle(self):
		return self.__title

	def _getLink(self):
		return self.__link

	def __repr__(self):
		return u"{0} ({1})".format(self.Title, self.Link)

	Title = property(_getTitle)
	Link = property(_getLink)

class TorrentFile(object):
	def __init__(self, title, link, content):
		self.__title = title
		self.__link = link
		self.__content = content

	def _getTitle(self):
		return self.__title

	def _getLink(self):
		return self.__link

	def _getContent(self):
		return self.__content

	def __repr__(self):
		return u"{0} ({1})".format(self.Title, self.Link)

	Title = property(_getTitle)
	Link = property(_getLink)
	Content = property(_getContent)

class XmlRpc(object):
	def __init__(self, uri, cookies):
		self.__uri = uri
		self.__cookies = cookies

	def loadstart(self, torrent):
		if not isinstance(torrent, TorrentFile):
			raise ValueError(u"Expected {0} but got {1} instead".format(TorrentFile, type(torrent)))

		# get the content of the torrent file
		torrentdata = torrent.Content

		# load raw start torrent
		import xmlrpclib
		proxy = xmlrpclib.ServerProxy(self.Uri, encoding='utf-8')
		arg1 = xmlrpclib.Binary(torrentdata)
		return proxy.load_raw_start(arg1)

	def _getUri(self):
		return self.__uri

	def _getCookies(self):
		return self.__cookies

	Uri = property(_getUri)
	Cookies = property(_getCookies)

class RSSFeed(object):
	def __init__(self, uri, cookies):
		self.__uri = uri
		self.__cookies = cookies

	def getTorrents(self):
		torrents = self._getTorrentsGenerator()
		return list(torrents)

	def getTorrentFile(self, torrent):
		if not isinstance(torrent, RSSTorrent):
			raise ValueError(u"Expected {0} but got {1} instead".format(RSSTorrent, type(torrent)))

		# fetch torrent content
		import requests
		r = requests.get(torrent.Link, cookies=self.Cookies)
		torrentdata = r.content

		return TorrentFile(torrent.Title, torrent.Link, torrentdata)


	def _getTorrentsGenerator(self):
		# fetch rss feed content
		import requests
		r = requests.get(self.Uri, cookies=self.Cookies)
		data = r.content

		# parse rss feed
		import feedparser
		feed = feedparser.parse(data)
		for item in feed["items"]:
			title = item["title"]
			link = item["link"]
			torrent = RSSTorrent(title, link)
			yield torrent

	def _getUri(self):
		return self.__uri

	def _getCookies(self):
		return self.__cookies

	Uri = property(_getUri)
	Cookies = property(_getCookies)

class CommandLineArguments(object):

	def _getArgument(self, arg, prefix):
		needle = u"{0}=".format(prefix)
		if arg.startswith(needle):
			return arg[len(needle):]
		return None

	def _getFirstArgument(self, prefix):
		# gets an argument prefixed by the given key
		# or None if it cannot be found
		for arg in sys.argv:
			argvalue = self._getArgument(arg, prefix)
			if argvalue:
				return argvalue
		return None

	def _getFirstRequiredArgument(self, prefix):
		result = self._getFirstArgument(prefix)
		if not result:
			raise ValueError(u"Missing required argument {0}".format(prefix))
		return result

	def _getRSSFeedUri(self):
		return self._getFirstRequiredArgument(u"--rss-feed-uri")

	def _getXmlRpcUri(self):
		return self._getFirstRequiredArgument(u"--xml-rpc-uri")

	def _getRSSFeedCookies(self):
		cookies = {}
		cookie_key = None
		cookie_value = None
		for arg in sys.argv:
			# check if argument is a cookie key
			cookie_key_value = self._getArgument(arg, u"--rss-feed-cookie-key")
			if cookie_key_value:
				cookie_key = cookie_key_value

			# check if argument is a cookie value
			cookie_value_value = self._getArgument(arg, u"--rss-feed-cookie-value")
			if cookie_value_value:
				cookie_value = cookie_value_value
				if not cookie_key:
					raise ValueError(u"Expected --rss-feed-cookie-key before {0}".format(arg))

			# check if both are set; store it and reset both
			if cookie_key and cookie_value:
				cookies[cookie_key] = cookie_value
				cookie_key = cookie_value = None
		return cookies

	def _getVerbose(self):
		value = self._getFirstArgument(u"--verbose")
		if value in [None, "yes"]:
			return True
		elif value in ["no"]:
			return False
		else:
			raise ValueError(u"Expected --verbose=[yes|no] but got --verbose={0} instead".format(value))
		
	RSSFeedUri = property(_getRSSFeedUri)
	XmlRpcUri = property(_getXmlRpcUri)
	RSSFeedCookies = property(_getRSSFeedCookies)
	Verbose = property(_getVerbose)

def main():
	# parse arguments
	commandlineargs = CommandLineArguments()
	rssuri = commandlineargs.RSSFeedUri
	xmlrpcuri = commandlineargs.XmlRpcUri
	rssfeedcookies = commandlineargs.RSSFeedCookies
	verbose = commandlineargs.Verbose

	# run
	rssfeed = RSSFeed(rssuri, rssfeedcookies)
	xmlrpc = XmlRpc(xmlrpcuri, rssfeedcookies)
	if verbose:
		sys.stdout.write(u"Fetching rss feeds .. ")
	torrents = rssfeed.getTorrents()
	if verbose:
		print u"OK"
	for torrent in torrents:
		if verbose:
			sys.stdout.write(u"Fetch torrent file for {0} .. ".format(torrent.Title))
		torrentfile = rssfeed.getTorrentFile(torrent)
		if verbose:
			print u"OK"
			print sys.stdout.write(u"Loadstart {0} .. ".format(torrent.Title))
		xmlrpc.loadstart(torrentfile)
		if verbose:
			print u"OK"
	if verbose:
		print u"Work done, bye!"

if __name__ == '__main__':
	main()
