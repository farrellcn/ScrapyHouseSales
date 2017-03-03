#coding=utf-8

import pymysql.cursors

class DBOperator():

	def __init__(self, serverAddr, serverPort, userName, passwd, dbName):
		self.conn = pymysql.connect(host=serverAddr,
                             port=serverPort,
                             user=userName,
                             password=passwd,
                             db=dbName,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.close()

	def Execute(self, sqlStr):
		#print (sqlStr)
		row = self.cursor.execute(sqlStr)
		self.conn.commit()
		return row

	def ExecuteMany(self, sqlStr, param):
		row = self.cursor.executemany(sqlStr, param)
		self.conn.commit()
		return row

	def GetLastRecords(self):
		return self.cursor.fetchall()
