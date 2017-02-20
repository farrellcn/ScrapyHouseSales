#list = [
    #['11', ' 0', " 'MMB'", " '2 MB INTERNATIONAL'", ' NULL', ' NULL', ' 0'],
    #['12', ' 0', " '3D STRUCTURES'", " '3D STRUCTURES'", ' NULL', ' NULL', ' 0'],
    #['13', ' 0', " '2 STRUCTURES'", " '2D STRUCTURES'", ' NULL', ' NULL', ' 0']]

#for elem in list:
#    print ('INSERT INTO "Tbl_ABS" VALUES (%s, %s, %s, %s, %s, %s, %s)' % tuple(elem))
from DBOperator import DBOperator
from datetime import *
import time
import uuid, configparser, sys, collections

CONFIG_FILE_NAME = 'config.ini'
CONFIG_FIELD_EMAIL = 'email'
CONFIG_FIELD_DATABASE = 'database'

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
	return ''
	#return os.path.dirname(sys.argv[0]) + '\\'

dbHost = ReadConfig(CONFIG_FIELD_DATABASE, 'host')
dbPort = int(ReadConfig(CONFIG_FIELD_DATABASE, 'port'))
dbName = ReadConfig(CONFIG_FIELD_DATABASE, 'dbName')
dbUser = ReadConfig(CONFIG_FIELD_DATABASE, 'user')
dbPassword = ReadConfig(CONFIG_FIELD_DATABASE, 'password')
db = DBOperator(dbHost, dbPort, dbUser, dbPassword, dbName)

for i in range(0,9):
	print (i)

print (uuid.uuid1())
print (uuid.uuid1())
print (uuid.uuid1())
time.sleep(100)
print (uuid.uuid1())
print (uuid.uuid1())

dicta = {'title': '寿县', 'community': '寿春苑'}


listA = list(dicta.values())
print (listA)
c = tuple(dicta.keys())
print (c)

productUpdateTime = '1小时'
result = datetime.now()
if len(productUpdateTime) == 0:
	result = datetime.now() + timedelta(days = -1)
elif productUpdateTime.find('小时') > -1:
	hourCount = int(productUpdateTime[0: productUpdateTime.find('小时')])
	result = datetime.now() + timedelta(hours = -hourCount)
elif productUpdateTime.find('分钟') > -1:
	minuteCount = int(productUpdateTime[0: productUpdateTime.find('分钟')])
	result = datetime.now() + timedelta(minutes = -minuteCount)
elif productUpdateTime.count('-') > 0:
	if productUpdateTime.count('-') == 1:
		productUpdateTime = datetime.strftime(result, '%Y-') + productUpdateTime
	result = datetime.strptime(productUpdateTime, "%Y-%m-%d")
print (datetime.strftime(result, '%Y-%m-%d'))
#sqlStr = 'INSERT INTO secondhand (:title)'

#db = DBOperator(dbHost, dbPort, dbUser, dbPassword, dbName)
#row = db.Execute('SELECT * FROM secondhand')