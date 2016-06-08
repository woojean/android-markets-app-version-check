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
from urllib import quote



'''
,
	{
		"tag":"ruan8",
		"name":"软吧",
		"url":"http://www.ruan8.com/search.php?stype=12&keyword=$$$",
		"l":"<ul class=\"mdccs\"",
		"r":"</ul>",
		"detail":{
			"l":"<span class=listname",
			"r":"</a>",
		}
	}
'''



def parseVersion(s,l,r):
	v = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	pattern=re.compile(VERSION_PATTEN)
	suspects = pattern.findall(s)
	if(len(suspects)>1):
		for suspect in suspects:
			if suspect.count('.') > 1:
				v = suspect
				break
	else:
		v = suspects[0]
	return v

def getDetailUrl(s,l,r):
	link = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	href = parseHref(s)
	return href

def parseHref(s):
	href = ''
	pattern=re.compile(HREF_PATTEN)
	suspects = pattern.findall(s)
	print suspects
	
	if(len(suspects) > 0 ):
		href = suspects[0]
	return href

VERSION_PATTEN = '\d+[\.|\d]+\d+'
#HREF_PATTEN = '<a.*?href="(.+)".*?>(.*?)</a>'
HREF_PATTEN = 'href=\"(.+?)\"'

if __name__ == '__main__':
	s = open('log.txt','r').read()
	l = "<span class=listname"
	r = "</a>"
	print getDetailUrl(s,l,r)



