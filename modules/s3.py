#coding=utf-8
"""This module contains classes for interacting with Amazon S3,
   including an extension for boto.s3.key.Key
"""
from boto.s3.connection import S3Connection as _S3Connection
from boto.s3.key import Key as BotoKey

class Key(BotoKey):
	"""extends Amazon's key class with name splitting,
	   to get “files” and “folders”. This is the class
	   returned by S3Connection:getNext yielder
	"""
	def __init__(self,bucket=None, key=None):
		super(Key, self).__init__(bucket, key.name)
		if key is not None:
			self.name = key.name.encode('utf-8')
			self.filename = self.name.split("/")[-1]
			self.extension = self.filename.split(".")[-1]
			self.basename = self.filename.split(".")[0]

class S3Connection(object):
	"""Represents a S3 connection
	"""
	def __init__(self,
		aws_access_key_id,
		aws_secret_access_key,
		aws_bucket_name="protokollen"):
		self._conn = _S3Connection(aws_access_key_id, aws_secret_access_key)
		self._bucket = self._conn.get_bucket(aws_bucket_name)

	def getNextFile(self):
		for key in self._bucket.list():
			yield Key(self._bucket,key)

	def getBucketListLength(self,pathFragment):
		l = self._bucket.list(pathFragment)
		i = 0
		for key in l:
			i += 1
		return i

	def fileExistsInBucket(self,fullfilename):
		if self.getBucketListLength(fullfilename):
			return True
		else:
			return False

	def putFile(self,localFilename,s3name):
		k = Key(self._bucket,s3name)
		k.set_contents_from_filename(localFilename)

if __name__ == "__main__":
	print "This module is only intended to be called from other scripts."
	import sys
	sys.exit()