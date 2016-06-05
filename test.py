#-*- coding: UTF-8 -*-  
# @author woojean https://github.com/woojean
# email:168056828@qq.com

import os
import sys
import datetime
import string
import time
import re
import platform
import urllib2
import json


def doRequest(url):
	try:
		req = urllib2.Request(url) 
		res = urllib2.urlopen( req ) 
		raw_data = res.read() 
		res.close()
	except Exception, ex:
		print('Error: Access trace service failed![%s]' % str(ex))
		return None
	return raw_data


def parseVersion(s,l,r):
	v = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	pattern=re.compile('\d+[\.|\d]+\d+')
	suspects = pattern.findall(s)
	if(len(suspects)>1):
		for suspect in suspects:
			if suspect.count('.') > 1:
				v = suspect
				break
	return v

def loadConfig(file):
	f = open(file,'r').read()
	config = eval(f)
	return config

def parseDetailUrl(s,l,r):
	v = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	pattern=re.compile('\d+[\.|\d]+\d+')
	suspects = pattern.findall(s)
	print suspects

def doPost(posturl,postdata):
	cookies = urllib2.HTTPCookieProcessor()
	opener = urllib2.build_opener(cookies)
	request = urllib2.Request(
        url     = posturl,
        headers = {
        	'Accept':"application/json, text/javascript, */*; q=0.01",
        	'X-Requested-With': 'XMLHttpRequest',
        	'Origin':'http://android.myapp.com'
        },
        data    = ''
    )
	f = opener.open(request)
	return f

# 如果 v1 >= v2，则返回true
def versionCompare(v1,v2):
	arr1 = v1.split('.')
	arr2 = v2.split('.')
	length = len(arr1)
	if(len(arr2) < length):
		length = len(arr2)
	for i in range(0,length):
		if(int(arr1[i]) >= int(arr2[i])):
			return True
	return False


if __name__ == '__main__':
	s = 'v2.0'
	pattern=re.compile('\d+[\.|\d]+\d+')
	suspects = pattern.findall(s)
	print suspects