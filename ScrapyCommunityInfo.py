#coding=utf-8

from datetime import *
from enum import Enum
from xml.dom import minidom
from email.mime.text import MIMEText
from email.header import Header
from DBOperator import DBOperator
import urllib.request, re, codecs, os, os.path, smtplib, configparser, time, sys, uuid

XML_FILE_NAME = 'ScrapyHouseSales.xml'
SOURCE_NODE_NAME = 'Source'

PATH_CONFIG = 'config/'
CONFIG_FILE_NAME = 'config.ini'
CONFIG_FIELD_EMAIL = 'email'
CONFIG_FIELD_DATABASE = 'database'

PATH_LOG = 'log/'
LOG_FILE_NAME = 'log.txt'

SCRAPY_CAUSE_New = 'New'
SCRAPY_CAUSE_TimeUpdate = 'TimeUpdate'
SCRAPY_CAUSE_PriceChange = 'PriceChange'
SCRAPY_CAUSE_ContentChange = 'ContentChange'
SCRAPY_CAUSE_PriceRise = 'PriceRise'
SCRAPY_CAUSE_PriceReduce = 'PriceReduce'

#读ini文件
def ReadConfig(field, key):
    cf = configparser.ConfigParser()
    try:
    	cf.read(GetConfigPath() + CONFIG_FILE_NAME)
    	result = cf.get(field, key)
    except:
    	Log('Read config file wrong: field=%s,key=%s', (field, key))
    	sys.exit(1)
    return result

#写ini文件
def WriteConfig(field, key, value):
    cf = configparser.ConfigParser()
    try:
        cf.read(CONFIG_FILE_NAME)
        cf.set(field, key, value)
        cf.write(open(GetConfigPath() + CONFIG_FILE_NAME,'w'))
    except:
        sys.exit(1)
    return True

def IsNum(str):	
	try:
		float(str)
		return True
	except ValueError as e:
		return False

def IsInt(str):	
	try:
		int(str)
		return True
	except ValueError as e:
		return False

def GetAbsPath():
	'''
	sys.argv为执行该python脚本时的命令行参数
	sys.argv[0]为该python脚本的路径
	'''	
	if len(os.path.dirname(sys.argv[0])) < 1:
		return ''
	else:
		return os.path.dirname(sys.argv[0]) + '/'

def GetLogPath():
	return GetAbsPath() + PATH_LOG

def GetConfigPath():
	return GetAbsPath() + PATH_CONFIG

#将新发布的卖房信息添加到数据库
def AddToDatabase(houseList):
	if len(houseList) < 1:
		return
	notify = 1	
	if len(houseList[0].data.keys()) < 0:
		return
	formatStr = ''
	for i in range(0, len(houseList[0].data.keys())):
		formatStr = formatStr + '%s,'
	formatStr = formatStr[0: len(formatStr) - 1]
	keyList = str(tuple(houseList[0].data.keys()))
	keyList = keyList.replace('\'', '')
	keyList = keyList.replace('(', '')
	keyList = keyList.replace(')', '')
	sqlInsert = 'INSERT INTO secondhand(notify, %s) VALUES(%d, %s)' % (keyList, notify, formatStr)
	records = []
	
	for house in houseList:
		param = list(house.data.values())
		records.append(param)
	db.ExecuteMany(sqlInsert, records)


def Log(logStr):
	logPath = GetLogPath()
	if not os.path.exists(logPath):
		os.mkdir(logPath)
	logFile =logPath + LOG_FILE_NAME
	fpLog = open(logFile, 'a')
	nowTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
	fpLog.write('%s  %s\n' % (nowTime, logStr))
	fpLog.close()

class HtmlInputList(SGMLParser):
	def __init__(self, postFields):
		self.reset()
		for field in postFields:
			self.spans[field.name] = ''
		
	def reset(self):		
		SGMLParser.reset(self)
		self.isKey = False;
		self.spans = {}	

	def start_span(self, attrs):
		self.isKey = False
		name = ''
		if attrs.has_key('id'):		
			if attrs['id'].strip() in self.spans.keys:
				self.isKey = True

	def handle_data(self, text)
		if self.isKey:
			print (text)

class Field():
	def __init__(self, sourceField):
		if sourceField != None:
			self.name = sourceField.name
			self.elementID = sourceField.elementID
			self.formatStr = sourceField.formatStr
			self.defaultValue = sourceField.defaultValue
			self.fixedValue = sourceField.fixedValue

		def GetValue(self, name):
			if FieldDataType.dtInteger == self.dataType:
				return int(self.value)
			elif FieldDataType.dtBoolean == self.dataType:
				return bool(self.value)
			else:
				return self.value


#邮件通知类
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
			print ('prepare send mail To: %s' % self.sendTo)
			#print ('smtp: %s port: %s from: %s to: %s password: %s' % (self.smtp, self.port, self.sendFrom, self.sendTo, self.password))
			smptObj = smtplib.SMTP(self.smtp, self.port)
			#smptObj.set_debuglevel(1)
			smptObj.login(self.sendFrom, self.password)
			smptObj.sendmail(self.sendFrom, [self.sendTo], message.as_string())
			smptObj.quit()
			print ('send mail success')
			return True
		except smtplib.SMTPException:			
			print ('send mail fail')
			return False
		return False

class PreSaleInfo():
	title = ''
	community = ''
	location = ''
	description = ''
	tag = ''
	publisherType = ''
	publisherName = ''
	constructorTime = ''
	floor = 0
	buildingFloors = 0
	orientation = ''
	layout = ''
	square = ''
	price = 0.0 #价格
	unit = '' #价格单位
	unitPrice = 0.0 #每平方单价
	buildingType = '' #房型
	decoration = ''
	productUpdateTime = ''
	tel = ''
	url = ''
	source = ''
	remark = ''
	pic = ''
	def __init__(self):
		self.data = {'title': ''}

class FieldDataType(Enum):
    dtString = 1
    dtInteger = 2
    dtBoolean = 3

    def stringToDataType(typeStr):
    	if typeStr == '_INT':
    		return FieldDataType.dtInteger
    	elif typeStr == '_BOOL':
    		return FieldDataType.dtBoolean
    	else:
    		return FieldDataType.dtString

class PageSearchMode(Enum):
	smInit = 1	#首次抓取该网站
	smAdd  = 2	#非首次抓取该网站

class Field():
	def __init__(self, sourceField):
		if sourceField != None:
			self.name = sourceField.name
			self.dataType = sourceField.dataType
			self.matchGroupIndex = sourceField.matchGroupIndex

		def GetValue(self, name):
			if FieldDataType.dtInteger == self.dataType:
				return int(self.value)
			elif FieldDataType.dtBoolean == self.dataType:
				return bool(self.value)
			else:
				return self.value


class PageListInfo():
	def __init__(self, node):
		self.charset = node.getElementsByTagName('Charset')[0].childNodes[0].nodeValue					#该网站的字符编码，解析页面的时候需要用
		self.baseUrl = node.getElementsByTagName('BaseUrl')[0].childNodes[0].nodeValue					#该网站的起始搜索页
		self.nextPage = node.getElementsByTagName('NextPage')[0].childNodes[0].nodeValue				#该网站的下一页
		self.searchDeep = int(node.getElementsByTagName('SearchDeep')[0].childNodes[0].nodeValue)		#每次检查更新的搜索深度
		self.maxDeep = int(node.getElementsByTagName('MaxDeep')[0].childNodes[0].nodeValue)				#首次爬取该网站的搜索深度
		self.regex = node.getElementsByTagName('Regex')[0].childNodes[0].nodeValue						#售房信息提取正则表达式
		self.htmlTemplate = node.getElementsByTagName('HtmlTemplate')[0].childNodes[0].nodeValue		#html模板，用于生成邮件内容
		self.SummaryTemplate = node.getElementsByTagName('SummaryTemplate')[0].childNodes[0].nodeValue	#售房概览信息
		dataFieldsNode = node.getElementsByTagName('DataFields')[0]
		fieldList = dataFieldsNode.getElementsByTagName('Field')
		self.fields = []
		for fieldNode in fieldList:
			field = Field(None)
			field.name = fieldNode.getAttribute('Name')
			field.dataType = FieldDataType.stringToDataType(fieldNode.getAttribute('DataType'))
			field.matchGroupIndex = int(fieldNode.getAttribute('MatchGroupIndex'))
			self.fields.append(field)

class HtmlContent():
	def __init__(self):
		self.count = 0
		self.html = ''

class ScrapyPreSaleInfo():
	#从配置文件加载爬取网站所需的信息
	def LoadConfig(self):
		dom = minidom.parse(GetConfigPath() + XML_FILE_NAME)
		root = dom.documentElement
		sourceNodeList = root.getElementsByTagName(SOURCE_NODE_NAME)
		for sourceNode in sourceNodeList:
			if self.source == sourceNode.getAttribute('Name'):
				print ('Source = ' + self.source)
				pageListNode = sourceNode.getElementsByTagName('PageList')[0]
				self.pageList = PageListInfo(pageListNode)

	def __init__(self, sourceName):
		self.pageCount = 0
		self.searchMode = self.GetSearchMode(sourceName)
		self.preSaleList = []

	def GetSearchMode(self, sourceName):
		row = db.Execute('SELECT COUNT(*) AS recordCount FROM presaleinfo WHERE Source="%s"' % sourceName)
		if row > 0:
			records = db.GetLastRecords()
			firshRecord = records[0]
			if int(firshRecord['recordCount']) > 0:	
				print ('Increment Scrapy')
				return PageSearchMode.smAdd
		print ('Collection Scrapy')
		return PageSearchMode.smInit

	def SearchPreSale(self):
		if self.pageCount >= self.pageList.maxDeep:
			return False
		if self.searchMode == PageSearchMode.smInit:
			print ('Continue Scrapy')
			return True
		if self.currentPageUrl == self.pageList.baseUrl:
			return True
		if self.pageCount >= self.pageList.searchDeep:
			return False
		return True

	def GetHtml(self, subscriber):
		htmlObj = HtmlContent()
		houseStr = ''		
		for house in self.houseList:
			if not self.NeedNotify(house):
				continue
			htmlObj.count = htmlObj.count + 1
			houseStr = self.pageList.htmlTemplate
			for key in house.data:
				if key == 'scrapyCause':
					houseStr = houseStr.replace('$' + key + '$', causeDic[house.data[key]], 1)
				else:
					houseStr = houseStr.replace('$' + key + '$', house.data[key], 1)
			htmlObj.html = htmlObj.html + houseStr
		print ('html finished')
		return htmlObj

	def NeedNotify(self, house):
		if house.data['scrapyCause'] == SCRAPY_CAUSE_TimeUpdate:
			return False
		return True

	def GetSummaryText(self, house):
		summaryText = self.pageList.SummaryTemplate		
		for key in house.data:
			summaryText = summaryText.replace('$' + key + '$', house.data[key], 1)
		return summaryText	

	def Scrapy(self):
		self.currentPageUrl = self.pageList.baseUrl;
		while self.SearchPreSale():
			print ('Scrapy: ' + self.currentPageUrl)
			self.pageCount = self.pageCount + 1
			pageContent = self.GetPageContent(self.currentPageUrl)
			if len(pageContent) > 0:
				pageContent = pageContent.decode(self.pageList.charset)	
				matchList = re.findall(self.pageList.regex, pageContent)
				if len(matchList) < 1:
					print ('There is no house on this page, Stop search')
					break
				for match in matchList:
					house = PreSaleInfo()
					for field in self.pageList.fields:
						house.data['source'] = self.source
						house.data['guid'] = str(uuid.uuid1())
						if field.matchGroupIndex < len(match):
							house.data[field.name] = match[field.matchGroupIndex].strip()									
					self.ProcessSpecField(house.data)
					house.data['summaryText'] = self.GetSummaryText(house)
					createTime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
					updatetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
					house.data['createTime'] = createTime
					house.data['updatetime'] = updatetime
					if len(house.data['productID']) < 1:
						house.data['productID'] = str(createTime)				
					if self.IsNewly(house):					
						self.houseList.append(house)
			self.currentPageUrl = self.GetNextPage()
		Log('Scrapy [%s] finish' % self.source)

	def ProcessSpecField(self, dataDict):
		dataDict['productUpdateTime'] = dataDict['productUpdateTimeStr']

	#是否有新添加的售房信息
	def IsNewly(self, house):
		#print (house.data['summaryText'])
		row = db.Execute('SELECT * FROM presaleinfo WHERE ProjectID="%s"' % house.data['projectID'])
		if row > 0:
			return False		
		return True

	def GetPageContent(self, pageurl):
		try:
			response = urllib.request.urlopen(pageurl)
		except:
			print ('can''t get page')
			return ('')
		return response.read()

	def GetNextPage(self):
		match = re.search(self.pageList.nextPage, self.currentPageUrl)
		if match != None:
			currPageNo = int(match.group(1))
			currPageNo = currPageNo + 1
			return re.sub('\(\\\d\+\)', str(currPageNo), self.pageList.nextPage)
		else:
			return ''

#reload(sys)
#sys.setdefaultencoding('utf8')
Log('=============================')
Log('Application Start')

causeDic = {SCRAPY_CAUSE_New : '新增', SCRAPY_CAUSE_TimeUpdate : '更新', SCRAPY_CAUSE_PriceChange : '价变', SCRAPY_CAUSE_ContentChange : '修改', SCRAPY_CAUSE_PriceRise : '涨价', SCRAPY_CAUSE_PriceReduce : '降价'}
dbHost = ReadConfig(CONFIG_FIELD_DATABASE, 'host')
dbPort = int(ReadConfig(CONFIG_FIELD_DATABASE, 'port'))
dbName = ReadConfig(CONFIG_FIELD_DATABASE, 'dbName')
dbUser = ReadConfig(CONFIG_FIELD_DATABASE, 'user')
dbPassword = ReadConfig(CONFIG_FIELD_DATABASE, 'password')
db = DBOperator(dbHost, dbPort, dbUser, dbPassword, dbName)
Log('Connect Database Successful')

scrapyShoufc = ScrapyShouFC('shoufc')
scrapyShoufc.LoadConfig()
scrapyShoufc.Scrapy()

scrapy58 = Scrapy58('58')
scrapy58.LoadConfig()
scrapy58.Scrapy()

houseCount = (len(scrapy58.houseList) + len(scrapyShoufc.houseList))
Log('Newly Update House: %d' %houseCount)
if houseCount < 1:
	print ('No New')
else:
	writeDatabase = True
	mailContent = ''	
	satisfiedCount = 0	
	htmlObj = scrapyShoufc.GetHtml(mailContent)
	mailContent = mailContent + htmlObj.html
	satisfiedCount = satisfiedCount + htmlObj.count	
	htmlObj = scrapy58.GetHtml(mailContent)
	mailContent = mailContent + htmlObj.html
	satisfiedCount = satisfiedCount + htmlObj.count
	if satisfiedCount > 0:
		subject =  '新增房源：%d' % satisfiedCount
		Log('Newly Satisfied: %d' % satisfiedCount)
		notifyMgr = Notify()
		if notifyMgr.Send(subject, mailContent):			
			Log('Send Email Successful')
		else:
			writeDatabase = False
			Log('Send Email Fail')
	else:
		print ('No Satisfied')
	if writeDatabase:
		if len(scrapyShoufc.houseList) > 0:	
			AddToDatabase(scrapyShoufc.houseList)
		if len(scrapy58.houseList) > 0:
			AddToDatabase(scrapy58.houseList)
Log('Application Closed')
