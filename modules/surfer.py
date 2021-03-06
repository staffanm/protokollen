#coding=utf-8
import logging

class Surfer:
	"""This class does virtual web surfing on our demand
	"""
	def __init__(self,delay=2):
		self.extraDelay = delay #extra time to wait after each operation (s)
		from selenium import webdriver
		from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
		from selenium.webdriver.common.by import By
		from selenium.webdriver.support import expected_conditions as ExpectedConditions
		from xvfbwrapper import Xvfb

		self.vdisplay = Xvfb()
		self.vdisplay.start()

		self.selenium_profile = webdriver.FirefoxProfile()
		self.selenium_driver = webdriver.Firefox(self.selenium_profile)

	def surfTo(self,url):
		self.selenium_driver.get(url)
		self.selenium_driver.implicitly_wait(self.extraDelay)

	def clickOnStuff(self,xPath):
		elementList = self.selenium_driver.find_elements_by_xpath(xPath)
		if not elementList:
			logging.warning("No elements found for xPath `%s`" % xPath)
		else:
			for element in elementList:
				element.click()
			self.selenium_driver.implicitly_wait(self.extraDelay)

	def findElements(self,xPath):
		return self.selenium_driver.find_elements_by_xpath(xPath)

	def getUrlList(self,xPath):
		urlList = []
		elementList = self.findElements(xPath)
		for element in elementList:
			href = element.get_attribute("href")
			if href is not None:
				urlList.append(Url(href))
		return urlList#list of Url objects

	def kill(self):
		self.selenium_driver.close()
		self.vdisplay.stop()

import urlparse
class Url:
	"""Represents a url, from e.g. Surfer.getHrefList()
	"""
	def __init__(self,url):
		self.href = url

	def is_absolute(self):
		"""Check if url is absolute or relative"""
		return bool(urlparse.urlparse(self.href).netloc)

	def make_absolute(self, reference_url):
		"""Makes this Url absolute, by using the domain from reference_url.

		   Does not handle protocol relative URLs
		"""
		parse_object = urlparse(reference_url)
		url_base = parse_object.scheme + "://" + parse_object.netloc
		self.href = url_base + self.href

if __name__ == "__main__":
	print "This module is only intended to be called from other scripts."
	import sys
	sys.exit()