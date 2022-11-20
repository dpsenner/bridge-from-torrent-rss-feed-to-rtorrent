#!/usr/bin/python3
import sys
import traceback
from requests.exceptions import ConnectionError

class RSSTorrent(object):
	def __init__(self, title, link):
		self.__title = title
		self.__link = link

	def _getTitle(self):
		return self.__title

	def _getLink(self):
		return self.__link

	def __repr__(self):
		return "{0} ({1})".format(self.Title, self.Link)


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
		return "{0} ({1})".format(self.Title, self.Link)

	Title = property(_getTitle)
	Link = property(_getLink)
	Content = property(_getContent)

class XmlRpc(object):
	def __init__(self, uri, cookies):
		self.__uri = uri
		self.__cookies = cookies

	def loadstart(self, torrent):
		if not isinstance(torrent, TorrentFile):
			raise ValueError("Expected {0} but got {1} instead".format(TorrentFile, type(torrent)))

		# get the content of the torrent file
		torrentdata = torrent.Content

		# load raw start torrent
		import xmlrpc.client
		try:
			proxy = xmlrpc.client.ServerProxy(self.Uri, encoding='utf-8')
			arg1 = xmlrpc.client.Binary(torrentdata)
			return proxy.load.raw_start("", arg1)
		except xmlrpc.client.Error:
			_, ex, traceback = sys.exc_info()
			raise RuntimeError("Could not start {0}.\n{1}".format(torrent.Title, ex), traceback)

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
		items = list(torrents)
		return items

	def getTorrentFile(self, torrent):
		if not isinstance(torrent, RSSTorrent):
			raise ValueError("Expected {0} but got {1} instead".format(RSSTorrent, type(torrent)))

		# fetch torrent content
		try:
			import requests
			r = requests.get(torrent.Link, cookies=self.Cookies)
			torrentdata = r.content
			return TorrentFile(torrent.Title, torrent.Link, torrentdata)
		except requests.exceptions.ConnectionError:
			_, ex, traceback = sys.exc_info()
			raise RuntimeError("Could not fetch torrent file for {0}.\n{1}".format(torrent.Title, ex), traceback)

	def _getTorrentsGenerator(self):
		# fetch rss feed content
		import requests
		try:
			r = requests.get(self.Uri, cookies=self.Cookies)
		except requests.exceptions.ConnectionError:
			_, ex, traceback = sys.exc_info()
			raise RuntimeError("Could not fetch feed.\n{0}".format(ex), traceback)
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
		needle = "{0}=".format(prefix)
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
			raise ValueError("Missing required argument {0}".format(prefix))
		return result

	def _getRSSFeedUri(self):
		return self._getFirstRequiredArgument("--rss-feed-uri")

	def _getXmlRpcUri(self):
		return self._getFirstRequiredArgument("--xml-rpc-uri")

	def _getRSSFeedCookies(self):
		cookies = {}
		cookie_key = None
		cookie_value = None
		for arg in sys.argv:
			# check if argument is a cookie key
			cookie_key_value = self._getArgument(arg, "--rss-feed-cookie-key")
			if cookie_key_value:
				cookie_key = cookie_key_value

			# check if argument is a cookie value
			cookie_value_value = self._getArgument(arg, "--rss-feed-cookie-value")
			if cookie_value_value:
				cookie_value = cookie_value_value
				if not cookie_key:
					raise ValueError("Expected --rss-feed-cookie-key before {0}".format(arg))

			# check if both are set; store it and reset both
			if cookie_key and cookie_value:
				cookies[cookie_key] = cookie_value
				cookie_key = cookie_value = None
		return cookies

	def _getVerbose(self):
		value = self._getFirstArgument("--verbose")
		if value in [None, "yes"]:
			return True
		elif value in ["no"]:
			return False
		else:
			raise ValueError("Expected --verbose=[yes|no] but got --verbose={0} instead".format(value))
		
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
		sys.stdout.write("Fetching rss feed .. ")
		sys.stdout.flush()
	try:
		torrents = rssfeed.getTorrents()
		if verbose:
			print("OK")
	except Exception:
		return
	except RuntimeError:
		print("FAIL")
		traceback.print_exc()
		return
	if torrents:
		for torrent in torrents:
			if verbose:
				print("Processing torrent {0} ..".format(torrent.Title))
				sys.stdout.write("Fetching torrent file .. ")
				sys.stdout.flush()
			try:
				torrentfile = rssfeed.getTorrentFile(torrent)
				if verbose:
					print("OK")
			except RuntimeError:
				print("FAIL")
				traceback.print_exc()
				return
			if verbose:
				sys.stdout.write("Invoking loadstart .. ")
				sys.stdout.flush()
			try:
				xmlrpc.loadstart(torrentfile)
				if verbose:
					print("OK")
			except RuntimeError:
				print("FAIL")
				traceback.print_exc()
				return
	else:
		if verbose:
			print("Received no torrents from the rss feed.")
	if verbose:
		print("Work done, bye!")

if __name__ == '__main__':
	main()
