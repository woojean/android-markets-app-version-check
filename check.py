#-*- coding: UTF-8 -*-  
# @author woojean https://github.com/woojean
# email:wxjsyz@vip.qq.com

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

import threading

class Spider(threading.Thread):
	_parsedList = []  
	_market = None
	def __init__(self,market):  
		self._market = market
		threading.Thread.__init__(self)  

  	def _check(self):
  		market = self._market
  		version = ''
		passed = -1
		url = genRequestUrl(market['url'],appName)
		marketTag = market['tag']
		print(marketTag+' ...')
		try:
			# 应用宝 ajax -> json
			if('yingyongbao' == marketTag):
				jsonResult = json.loads(doRequest(url))
				mostSimilarAppName = jsonResult['obj']['appDetails'][0]['appName']
				mostSimilarAppName = mostSimilarAppName.encode('utf-8') # ！
				if(appName in mostSimilarAppName):
					version = jsonResult['obj']['appDetails'][0]['versionName']
				# 魅族 ajax -> json
			elif('meizu' == marketTag):
				url = genRequestUrl(market['url'],quote(appName))
				jsonResult = json.loads(doRequest(url))
				version = jsonResult['value']['list'][0]['version_name']
			# 百度 get -> html
			# 安卓网 get -> html
			elif('baidu' == marketTag
				or 'hiapk' == marketTag
				or 'coolapk' == marketTag):
				version = parseVersion(doRequest(url),market['l'],market['r'])
			elif('topber' == marketTag):
				url = (market['url']).replace('$$$',quote(appName))
				version = parseVersion(doRequest(url),market['l'],market['r'])
			# list->detail
			# 应用汇
			# 360 
			# 豌豆荚
			# 小米应用商店
			# 安智市场
			# 乐商店
			# 机锋网
			# ...
			elif(marketTag in ['appchina','360','wandoujia','mi','anzhi','lenovomm','gfan']):
				htmlStr = doRequest(url)
				href = getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailUrl = market['prefix']+href
				detailHtmlStr = doRequest(detailUrl)
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 华为应用市场
			# PP助手
			# oppo软件商店
			elif('hicloud' == marketTag
				or '25pp' == marketTag
				or 'oppomobile' == marketTag):
				url = (market['url']).replace('$$$',quote(appName))
				htmlStr = doRequest(url)
				href = getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailUrl = market['prefix']+href
				detailHtmlStr = doRequest(detailUrl)
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 软吧 list->detail Url encode使用gb2312
			elif('ruan8' == marketTag):
				url = genRequestUrl(market['url'],quote(appName.decode('utf-8').encode('gb2312')))
				url = url.encode('utf-8')
				htmlStr = doRequest(url)
				htmlStr = htmlStr.decode('gb2312').encode('utf-8')
				detailUrl = 'http://www.ruan8.com'+getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailHtmlStr = doRequest(detailUrl)
				detailHtmlStr = detailHtmlStr.decode('gbk').encode('utf-8')
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 手机世界 jsonp
			elif('3533' == marketTag):
				jsonResult = json.loads(doRequest(url))
				mostSimilarAppName = jsonResult['data'][0]['topic_cn']
				mostSimilarAppName = mostSimilarAppName.encode('utf-8') # ！
				if(appName in mostSimilarAppName):
					detailUrl = 'http://a.3533.com/ruanjian/'+jsonResult['data'][0]['id']+'.htm'
					version = parseVersion(doRequest(detailUrl),market['l'],market['r'])
			else:
				pass
		except Exception,e:  
			pass
		if('' != version and '' != targetVersion):
			if(versionCompare(version,targetVersion)):
				passed = 1
			else:
				passed = 0
		result = {
			'tag':market['tag'],
			'name':market['name'],
			'version':version,
			'url':url,
			'passed':passed
		}
		Spider._parsedList.append(result)

	def run(self):
		self._check()



def genRequestUrl(url,appName):
	return url.replace('$$$',appName)


def doRequest(url):
	try:
		req = urllib2.Request(url) 
		req.add_header('User-Agent', 'Mozilla 5.10')
		res = urllib2.urlopen( req ,timeout = 10) 
		raw = res.read() 
		res.close()
	except Exception, ex:
		print('Error: Access trace service failed![%s]' % str(ex))
		return None
	return raw


def parseHref(s):
	href = ''
	pattern=re.compile(HREF_PATTEN)
	suspects = pattern.findall(s)
	
	if(len(suspects) > 0 ):
		href = suspects[0]
	return href


def getDetailUrl(s,l,r):
	link = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	href = parseHref(s)
	return href


def log(s):
	with open('log.txt', 'a') as f:
		f.write(s)


def doCheck(appName,markets,targetVersion=''):
	checkResult = []
	length = len(markets)
	for market in markets:
		spider = Spider(market)
		spider.start()

	while(length > len(Spider._parsedList)):
		continue

	return Spider._parsedList

	'''
	for market in markets:
		version = ''
		passed = -1
		url = genRequestUrl(market['url'],appName)
		marketTag = market['tag']
		print(marketTag+' ...')
		try:
			# 应用宝 ajax -> json
			if('yingyongbao' == marketTag):
				jsonResult = json.loads(doRequest(url))
				mostSimilarAppName = jsonResult['obj']['appDetails'][0]['appName']
				mostSimilarAppName = mostSimilarAppName.encode('utf-8') # ！
				if(appName in mostSimilarAppName):
					version = jsonResult['obj']['appDetails'][0]['versionName']
			# 魅族 ajax -> json
			elif('meizu' == marketTag):
				url = genRequestUrl(market['url'],quote(appName))
				jsonResult = json.loads(doRequest(url))
				version = jsonResult['value']['list'][0]['version_name']
			# 百度 get -> html
			# 安卓网 get -> html
			elif('baidu' == marketTag
				or 'hiapk' == marketTag
				or 'coolapk' == marketTag):
				version = parseVersion(doRequest(url),market['l'],market['r'])
			elif('topber' == marketTag):
				url = (market['url']).replace('$$$',quote(appName))
				version = parseVersion(doRequest(url),market['l'],market['r'])
			# list->detail
			# 应用汇
			# 360 
			# 豌豆荚
			# 小米应用商店
			# 安智市场
			# 乐商店
			# 机锋网
			# ...
			elif(marketTag in ['appchina','360','wandoujia','mi','anzhi','lenovomm','gfan']):
				htmlStr = doRequest(url)
				href = getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailUrl = market['prefix']+href
				detailHtmlStr = doRequest(detailUrl)
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 华为应用市场
			# PP助手
			# oppo软件商店
			elif('hicloud' == marketTag
				or '25pp' == marketTag
				or 'oppomobile' == marketTag):
				url = (market['url']).replace('$$$',quote(appName))
				htmlStr = doRequest(url)
				href = getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailUrl = market['prefix']+href
				detailHtmlStr = doRequest(detailUrl)
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 软吧 list->detail Url encode使用gb2312
			elif('ruan8' == marketTag):
				url = genRequestUrl(market['url'],quote(appName.decode('utf-8').encode('gb2312')))
				url = url.encode('utf-8')
				htmlStr = doRequest(url)
				htmlStr = htmlStr.decode('gb2312').encode('utf-8')
				detailUrl = 'http://www.ruan8.com'+getDetailUrl(htmlStr,market['detail']['l'],market['detail']['r'])
				detailHtmlStr = doRequest(detailUrl)
				detailHtmlStr = detailHtmlStr.decode('gbk').encode('utf-8')
				version = parseVersion(detailHtmlStr,market['l'],market['r'])
			# 手机世界 jsonp
			elif('3533' == marketTag):
				jsonResult = json.loads(doRequest(url))
				mostSimilarAppName = jsonResult['data'][0]['topic_cn']
				mostSimilarAppName = mostSimilarAppName.encode('utf-8') # ！
				if(appName in mostSimilarAppName):
					detailUrl = 'http://a.3533.com/ruanjian/'+jsonResult['data'][0]['id']+'.htm'
					version = parseVersion(doRequest(detailUrl),market['l'],market['r'])
			else:
				pass
		except Exception,e:  
			pass
		if('' != version and '' != targetVersion):
			if(versionCompare(version,targetVersion)):
				passed = 1
			else:
				passed = 0
		result = {
			'tag':market['tag'],
			'name':market['name'],
			'version':version,
			'url':url,
			'passed':passed
		}
		checkResult.append(result)
	return checkResult
	'''


# 如果 v1 >= v2，则返回true
def versionCompare(v1,v2):
	arr1 = v1.split('.')
	arr2 = v2.split('.')
	length = len(arr1)
	if(len(arr2) < length):
		length = len(arr2)
	for i in range(0,length):
		if(int(arr1[i]) > int(arr2[i])):
			return True
		elif(int(arr1[i]) < int(arr2[i])):
			return False
		else:
			continue
	if(len(arr2) > len(arr1)):
		return False
	else:
		return True


def dumpReport(appName,checkResult,targetVersion = ''):
	print('\n')
	html = '<html><head><meta charset="UTF-8"><style>$style$</style></head><body>\
	<div class="result">\
		<label>应用名称：<span>$appName$</span><label/><br/>\
		<label>比对版本：<span>$targetVersion$</span><label/><br/>\
		<label>检查时间：<span>$now$</span><label/><br/><br/>\
		<table cellspacing="0" summary="amavc check result">\
		<caption>Android应用市场最新版本检查结果</caption> \
		<tr>\
			<th class="tablehead"></th>\
			<th class="tablehead">应用市场名称</th>\
			<th class="tablehead">当前版本</th>\
			<th class="tablehead">是否最新</th>\
			<th class="tablehead"></th>\
		</tr>\
		$trs$</table>\
		<div class="from">\
			generated by <a href="https://github.com/woojean/amavc">amavc</a>\
		</div>\
	</div>\
	</body></html>'
	now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	date = time.strftime("%Y-%m-%d",time.localtime(time.time()))
	trs = ''
	rowStyle = True
	num = 1
	for result in checkResult:
		styleStr = "spec"
		if(rowStyle):
			rowStyle = False
			styleStr = "specalt"
			
		tr = '<tr>\
		<th class="'+styleStr+'">'+str(num)+'</td>\
		<th class="'+styleStr+'">$name$</td>\
		<td>$version$</td>\
		<td>$passed$</td>\
		<td><a target="_blank" href="$url$">查看详情</a></td>\
		</tr>'
		tr = tr.replace('$name$',result['name']).replace('$url$',result['url'])
		if(1 == result['passed']):
			tr = tr.replace('$version$','<font color="green">'+str(result['version']))+'</font>'
			tr = tr.replace('$passed$','<font color="green">已是最新</font>')
		elif( 0 == result['passed'] ):
			tr = tr.replace('$version$','<font color="red">'+str(result['version']))+'</font>'
			tr = tr.replace('$passed$','<font color="red">不是最新</font>')
		else:
			tr = tr.replace('$version$','<font color="black">'+str(result['version']))+'</font>'
			tr = tr.replace('$passed$','<font color="black">未知</font>')
		trs += tr
		num += 1
	html = html.replace('$style$',STYLE).replace('$appName$',appName).replace('$now$',now).replace('$trs$',trs)
	if('' != targetVersion):
		html = html.replace('$targetVersion$',targetVersion)
	else:
		html = html.replace('$targetVersion$','未指定')
	#html = html.encode('utf-8','ignore')
	
	reportFile = os.path.join('reports',date+'.html')
	jsonFile = os.path.join('reports',date+'.json')
	
	jsonResult = {
		'appName':appName,
		'targetVersion':targetVersion,
		'date':date,
		'checkReult':checkResult
	}

	try:
		jsonStr = json.dumps(jsonResult)
		with open(jsonFile, 'w') as f:
			f.write(jsonStr)

		with open(reportFile, 'w') as f:
			f.write(html)

		print('json file generated at '+jsonFile)
		print('report file generated at '+reportFile)
	finally:
		pass

def loadConfig(file):
	f = open(file,'r').read()
	config = eval(f)
	return config


def parseVersion(s,l,r):
	v = ''
	indexL = s.index(l)
	s = s[indexL:]
	indexR = s.index(r)
	s = s[:indexR]
	pattern=re.compile(VERSION_PATTEN)
	suspects = pattern.findall(s)
	print(suspects)
	if(len(suspects)>1):
		for suspect in suspects:
			if(len(suspect.split('.')[0])>3):
				continue
			elif(suspect.count('.') > 1):
				v = suspect
				break
	else:
		v = suspects[0]
	return v


STYLE = '''body {color: #4f6b72;}a {color: #c75f3e;}label{font: bold 1.2em;}span{font: normal 1.2em;}table {width: 100%;padding: 0;margin: 0;border:1px;border-radius:0.8em;}caption {padding: 0 0 5px 0;width: 100%;	 font: italic 1em 'Trebuchet MS', Verdana, Arial, Helvetica, sans-serif;text-align: right;}th {font: bold 1em 'Trebuchet MS', Verdana, Arial, Helvetica, sans-serif;color: #4f6b72;border-left: 1px solid #C1DAD7;border-right: 1px solid #C1DAD7;border-bottom: 1px solid #C1DAD7;border-top: 1px solid #C1DAD7;letter-spacing: 2px;text-transform: uppercase;text-align: center;padding: 6px 6px 6px 12px;background: white;}th.nobg {border-top: 0;border-left: 0;border-right: 1px solid #C1DAD7;background: none;}td {border-right: 1px solid #C1DAD7;border-bottom: 1px solid #C1DAD7;background: #fff;padding: 6px 6px 6px 12px;color: #4f6b72;text-align: center;}td.alt {background: #F5FAFA;color: #797268;}th.spec {border-left: 1px solid #C1DAD7;border-top: 0;font: bold 1em 'Trebuchet MS', Verdana, Arial, Helvetica, sans-serif;}th.specalt {border-left: 1px solid #C1DAD7;border-top: 0;font: bold 1em 'Trebuchet MS', Verdana, Arial, Helvetica, sans-serif;color: #797268;}.result {width:55%;background: #eee;padding:40px;padding-bottom:20px;margin-top:40px;margin-left:auto;margin-right:auto;}.tablehead{background: #ddd;font: lighter 1.1em 'Trebuchet MS', Verdana, Arial, Helvetica, sans-serif;}.from{margin-top:50px;text-align:right;}'''

VERSION_PATTEN = '\d+[\.|\d]+\d+'
HREF_PATTEN = 'href=\"(.+?)\"'

if __name__ == '__main__':
	appName = ''
	targetVersion = ''
	params = len(sys.argv)
	if(params < 2):
		exit(1)
	elif(2 == params):
		appName = sys.argv[1]
	elif(params > 2):
		appName = sys.argv[1]
		targetVersion = sys.argv[2]

	platformName = platform.system()
	if('Windows' == platformName):
		appName = appName.decode('gb2312').encode('utf-8')
		targetVersion = targetVersion.decode('gb2312').encode('utf-8')
		if(len(re.compile(VERSION_PATTEN).findall(targetVersion)) < 1):
			print 'invalid targetVersion code:'+ targetVersion
			exit(1)

	markets = loadConfig('config')
	result = doCheck(appName,markets,targetVersion)
	dumpReport(appName,result,targetVersion)
