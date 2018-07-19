#!/usr/bin/env python
# encoding: utf-8

"""
@author: xl7dev
@contact: root@safebuff.com
@time: 2017/3/19 下午8:44
"""
import os
import sys
import argparse
import logging
from time import sleep
from selenium import webdriver
from urlparse import urlparse

"""
brew install chromedriver
pip install selenium
"""


class Webscreenshot(object):
	def __init__(self):
		self.size = '1024x768'
		self.image = 2
		self.sleep = 0
		self.proxy = ''
		self.authproxy = ''
		self.useragent = 'Mozilla/5.0 (Windows NT 10.0; rv:50.0) Gecko/20100101 Firefox/50.0'
		self.driver = self.chromedriver()

	def chromedriver(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--window-size={0}'.format(self.size))
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--user-agent={0}".format(self.useragent))
		chrome_options.add_experimental_option("prefs",
											   {"profile.managed_default_content_settings.images": int(self.image)})
		chrome_options.add_argument('--proxy-server={0}'.format(self.proxy))
		if self.authproxy:
			chrome_options.add_extension(self.auth_proxy(self.authproxy))
		driver = webdriver.Chrome(self.chrome_binary(), chrome_options=chrome_options)
		driver.set_page_load_timeout(30)
		return driver

	def chrome_binary(self):
		path = os.path.dirname(os.path.abspath(__file__))
		if sys.platform.startswith('linux'):
			binary = 'bin/chromedriver_linux64'
		elif sys.platform.startswith('darwin'):
			binary = "bin/chromedriver_mac64"
		elif sys.platform.startswith('win'):
			binary = "bin/chromedriver_win32.exe"
		else:
			print "Not Found Google Chrome binary"
			exit()
		binary_location = r'{0}/{1}'.format(path, binary)
		return binary_location

	def loadurl(self, filename):
		urls = map(lambda x: x.strip() if x.startswith('http://') or x.startswith('https://') or x.startswith(
			'ftp://') else "http://" + x.strip(), open(filename))
		return list(set(urls))

	def worker(self, url):
		try:
			self.driver.get("%s" % url)
			sleep(self.sleep)
			filename = urlparse(url).netloc
			self.driver.save_screenshot('%s.png' % filename)
			print("{0} Success".format(filename))
		except Exception, e:
			logging.debug("URL: %s %s" % (url, e))


def main():
	demo = Webscreenshot()
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", help="increase output verbosity")
	parser.add_argument("-u", "--url", dest="url", help="Target URL (e.g. 'http://www.example.com')")
	parser.add_argument("-f", "--targets", dest="filename", help="Target From FILENAME", metavar="FILE")
	parser.add_argument("-image", "--image", dest="image", help="default disable image equal 2", metavar="FILE")
	parser.add_argument("-sleep", "--sleep", dest="sleep", help="default sleep equal 0")
	parser.add_argument("-size", "--size", dest="size", help="default size equal 1024x768")
	parser.add_argument("-proxy", "--proxy", dest="proxy",
						help="Proxy (e.g. 'http://127.0.0.1:1087' or 'socks5://127.0.0.1:1080')", metavar="proxy")
	args = parser.parse_args()
	if args.size:
		demo.size = args.size
	else:
		demo.size = '1024x768'
	if args.proxy:
		demo.proxy = args.proxy
	else:
		demo.proxy = ''
	if args.image:
		demo.image = args.image
	else:
		demo.image = 2
	if args.sleep:
		demo.sleep = args.sleep
	else:
		demo.sleep = 0
	if args.url:
		url = args.url if args.url.startswith('http://') or args.url.startswith('https://') or args.url.startswith(
			'ftp://') else "http://" + args.url
		demo.worker(url)
	elif args.filename:
		urls = demo.loadurl(args.filename)
		for url in urls:
			demo.worker(url)
	else:
		print "Use -h for help"
	demo.driver.quit()


if __name__ == "__main__":
	main()
"""
osx: brew install chromedriver
download chromedriver: https://chromedriver.storage.googleapis.com/index.html?path=2.37/
# platform options: linux32, linux64, mac64, win32
PLATFORM=linux64
VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip

http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver
"""
