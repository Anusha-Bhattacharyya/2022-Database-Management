import mysql.connector
from tabulate import tabulate

# host=turing.uark.edu,
# user=ab107,
# password=aijeNah8,
# database=ab107

class Connector:
	def open_database(self, hostname, user_name, mysql_pw, database_name):
		global conn
		try:
			conn = mysql.connector.connect(host=hostname,
										   user=user_name,
										   password=mysql_pw,
										   database=database_name
										   )
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else:
			global cursor
			cursor = conn.cursor()
		
	def printFormat(self, result):
		header = []
		for cd in cursor.description:  # get headers
			header.append(cd[0])
		print('')
		print('Query Result:')
		print('')
		print(tabulate(result, headers=header))  # print results in table format
		print('')

	# select and display query

	def executeSelect(self, query):
		cursor.execute(query)
		self.printFormat(cursor.fetchall())

	def insert(self, table, values):
		query = "INSERT into " + table + " values (" + values + ")" + ';'
		cursor.execute(query)
		conn.commit()

	def executeUpdate(self, query):  # use this function for delete and update
		cursor.execute(query)
		conn.commit()

	def close_db(self):  # use this function to close db
		cursor.close()
		conn.close()
