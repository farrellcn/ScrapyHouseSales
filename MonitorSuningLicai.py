#coding=utf-8

from datetime import *
from enum import Enum
from xml.dom import minidom
from email.mime.text import MIMEText
from email.header import Header
import urllib.request, re, codecs, os, os.path, smtplib, configparser, time, sys, json

CONFIG_FILE_NAME = 'SuningConfig.ini'
CONFIG_FIELD_PAGE = 'page'
CONFIG_FIELD_EMAIL = 'email'

def ReadConfig(field, key):
    cf = configparser.ConfigParser()
    try:
        cf.read(GetAbsPath() + CONFIG_FILE_NAME)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result

def WriteConfig(field, key, value):
    cf = configparser.ConfigParser()
    try:
        cf.read(CONFIG_FILE_NAME)
        cf.set(field, key, value)
        cf.write(open(CONFIG_FILE_NAME,'w'))
    except:
        sys.exit(1)
    return True

def GetAbsPath():
	#return 'D:\ShenJia\OneDriver\OneDrive\Project\ScrapyHouseSales\\'
	#print (os.path.dirname(sys.argv[0]))
	return os.path.dirname(sys.argv[0]) + '\\'

class Notify():
	def __init__(self):
		self.smtp = ReadConfig(CONFIG_FIELD_EMAIL, 'smtp')
		self.sendFrom = ReadConfig(CONFIG_FIELD_EMAIL, 'from')
		self.sendTo = ReadConfig(CONFIG_FIELD_EMAIL, 'to')
		self.port = ReadConfig(CONFIG_FIELD_EMAIL, 'port')
		self.password = ReadConfig(CONFIG_FIELD_EMAIL, 'password')

	def Send(self, subject, content):
		message = MIMEText(content, 'html', 'utf-8')
		message['From'] = "ZMInfo" + "<" + self.sendFrom +">"
		message['To'] = "farrell" + "<" + self.sendTo +">"

		nowTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
		subject = nowTime + subject
		message['Subject'] = Header(subject, 'utf-8')
		try:
			print ('准备发送邮件To: %s' % self.sendTo)
			#print ('smtp: %s port: %s from: %s to: %s password: %s' % (self.smtp, self.port, self.sendFrom, self.sendTo, self.password))
			smptObj = smtplib.SMTP(self.smtp, self.port)
			#smptObj.set_debuglevel(1)
			smptObj.login(self.sendFrom, self.password)
			smptObj.sendmail(self.sendFrom, [self.sendTo], message.as_string())
			smptObj.quit()
			print ('邮件发送成功')
			return True
		except smtplib.SMTPException:			
			print ('无法发送邮件')
			return False
		return False

class LicaiProduct():
	def __init__(self):
		self.data = {'name': ''}

class MonitorLicai():

	def __init__(self):		
		self.baseUrl = ReadConfig(CONFIG_FIELD_PAGE, 'baseUrl')
		self.htmlTemplate = ReadConfig(CONFIG_FIELD_PAGE, 'htmlTemplate')
		print (self.htmlTemplate)	
		self.productList = []

	def GetHtml(self):		
		htmlText = ''
		productStr = ''
		for product in self.productList:
			productStr = self.htmlTemplate
			for key in product.data:
				productStr = productStr.replace('$' + key + '$', product.data[key], 1)
			htmlText = htmlText + productStr
		print ('html finished')
		fpw = open('licaiProductList.html', 'w')
		fpw.write(htmlText)
		fpw.close()
		return htmlText

	def Scrapy(self):
		self.currentPageUrl = self.baseUrl;
		print ('Scrapy: ' + self.currentPageUrl)
		pageContent = self.GetPageContent(self.currentPageUrl)
		pageContent = pageContent.decode('utf-8')
		fp = open('LicaiContent.txt', 'w')
		fp.write(pageContent)
		fp.close()
		jsonObj = json.loads(pageContent)
		print (int(jsonObj['total']))
		if int(jsonObj['total']) > 1:
			for productJson in jsonObj['lists']:
				#if (int(productJson['progress']) < 100) and (str(productJson['selloff']) != 'false'):
					product = LicaiProduct()
					for key in productJson:				
						product.data[key] = str(productJson[key])
					self.productList.append(product)
			#productList = json.loads(str(jsonObj['lists'])
			#for product in productList:
			#	print (product.keys())
			#matchList = re.findall(self.pageList.regex, pageContent)
			#for match in matchList:
			#	house = HouseInfo()
			#	#print ('group: ' +str(len(match)))
			#	for field in self.pageList.fields:
			#		house.data['source'] = self.source
			#		if field.matchGroupIndex < len(match):
			#			#print (field.matchGroupIndex)
			#			house.data[field.name] = match[field.matchGroupIndex].strip()
			#			#print (field.name + ': ' + house.data[field.name])						
			#	self.productList.append(house)
			#正则匹配请求的页面



		#for i to count
		#将正则匹配转换成房屋信息
		#如果该房屋信息是今天之前的 跳出 while
		#将房屋信息加到列表

		#GetNextPage

		#while true
	def GetPageContent(self, pageurl):
		# retrieve the result
		response = urllib.request.urlopen(pageurl)
		return response.read()

	def GetMatchList(self, content):
		return re.findall(pattern, content);

	def GetHouseInfoFromText(self, match):
		pass

	def GetNextPage(self):
		match = re.search(self.pageList.nextPage, self.currentPageUrl)
		if match != None:
			currPageNo = int(match.group(1))
			currPageNo = currPageNo + 1
			return re.sub('\(\\\d\+\)', str(currPageNo), self.pageList.nextPage)
		else:
			return ''

	def IsNewItem(self, item):
		item.updateTime >= date.today()

data1 = {'b':789,'c':456,'a':123}
data2 = {'a':123,'b':789,'c':456}
d1 = json.dumps(data1,sort_keys=True)
d2 = json.dumps(data2)
d3 = json.dumps(data2,sort_keys=True)
print (d1)
print (d2)
print (d3)
print (d1==d2)