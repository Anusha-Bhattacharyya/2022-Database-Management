import os.path
import csv

class DB:

	#default constructor--
	def __init__(self):
		self.num_record_data = 0;
		self.num_record_overflow = 0
		self.IsOPEN = True
		self.configtxt_file = None
		self.datatxt_file = None
		self.overflowtxt_file = None

		#create the database
		print("\nCreate new database")
		csv_file = input('Enter the name of your input file: ')
		self.configtxt_file = 'config.txt'
		self.datatxt_file = 'data.txt'
		self.overflowtxt_file = 'overflow.txt'
		self.config = open('config.txt', 'w+')
		self.data = open(self.datatxt_file, 'w+')
		self.overflow = open('overflow.txt', 'w+')
		self.overflow.write('')
		self.config.write('numrecords = 10')
		with open(csv_file, 'r') as inp, self.data as out:
			for line in inp:
				line = line.replace(',', ' ').rstrip("\n")
				spaces = 107 - (len(line) + line.count(" "))
				out.write(line)
				out.write(" " * spaces + "\n")
		self.IsOPEN = True

	#read the database--
	def readDB(self, filename, DBsize, rec_size):
		self.filestream = filename
		self.record_size = DBsize
		self.rec_size = rec_size
		
		if not os.path.isfile(self.filestream):
			print(str(self.filestream)+" not found")
		else:
			self.data = open(self.filestream, 'r')

	#open the database-- FIX
	def OpenDB(self):
		self.config = open(self.configtxt_file, 'r+')
		self.data = open(self.datatxt_file, 'r+')
		self.overflow = open(self.overflowtxt_file, 'r+')
		self.IsOPEN = True
	
	#isOpen--
	def IsOpen(self):
		if (self.data.closed and self.config.closed and self.overflow.closed):
			self.IsOPEN = False;
			print("IsOPEN is False")

	#read record method-
	def readRecord(self, recordNum, filename):
		self.flag = False
		id = state = city = name = "None"
		self.num_record_data = self.DBsize
		recordNum = recordNum - 1

		if recordNum >=0 and recordNum < self.num_record_data and filename == self.data:
			#print("data")
			#print(recordNum)
			self.data.seek(0,0)
			self.data.seek(recordNum*self.rec_size)
			#line = self.data.readline().rstrip('\n')
			line = self.data.readline()
			self.flag = True
		elif str(filename) == 'self.overflow':
			self.overflow.seek(0,0)
			for i, line in enumerate(self.overflow, 1):
				if id in line:
					line = self.overflow.readline().rstrip('\n')
					self.flag = True
		else: 
			print("Could not find record")
		
		if self.flag:
			id, state, city, name = line.split()
			if self.print:
				print(line)
				self.print = False

		self.record = dict({"ID":id,"state":state,"city":city,"name":name})

	#write record method-
	def writeRecord(self, id, state, city, name):
		filesize = os.path.getsize("overflow.txt")
		print(self.add)
		if self.add:
			line = id + ' ' + state + ' ' + city + ' ' + name + '\n'
			self.overflow.write(line)
			self.add = False
		elif self.delete or self.overwrite:
			for i, line in enumerate(self.overflow, 1):
				if id in line:
					line = id + ' ' + state + ' ' + city + ' ' + name + '\n'
					self.overflow.write(line)
			self.delete = False
			self.overwrite = False
		else:
			print("write failed")

	#print/display record method
	def printRecord(self, ans):
		self.print = True
		if(self.IsOPEN):
			if ans == "4":
				RecordID = input("Enter the record ID that you wish to display:")
				RecordNum = self.findRecord(RecordID)
				if self.whichFile == '1':
					self.readRecord(RecordNum, self.overflow)
				elif self.whichFile == '2':
					self.readRecord(RecordNum, self.data)
			if ans == "6":
				source = {}
				header1 = "ID"
				header2 = "State"
				header3 = "City"
				header4 = "Name"
				data = []
				for i in range(10):
					self.data.seek(0,0)
					lines = self.data.readline()
					line = lines.strip()
					columns = line.split()
					spaces1 = 10 - len(columns[0])
					spaces2 = 20 - len(columns[1])
					spaces3 = 20 - len(columns[2])
					spaces4 = 60 - len(columns[3])
					source[header1] = columns[0] + (" " * spaces1)
					source[header2] = columns[1] + (" " * spaces2)
					source[header3] = columns[2] + (" " * spaces3)
					source[header4] = columns[3] + (" " * spaces4)
					data.append(source)
					print(source)

	#overwrite record method- 
	def overwriteRecord(self, recordNum, filename, id, state, city, name):
		self.overwrite = True
		self.readRecord(recordNum, filename)
		if (filename == self.data):
			self.data.seek(0,0)
			self.data.seek((recordNum - 1)*self.rec_size)
			line = id + ' ' + state + ' ' + city + ' ' + name
			spaces = 80 - (len(line) + line.count(" "))
			self.data.write(line)
			self.data.write(" " * spaces + "\n")
		elif(filename == self.overflow):
			writeRecord(id, state, city, name)
		else:
			print("overwrite failed")
	
	#Binary Search by record id--
	def binarySearch(self, input_ID):
		self.found = False
		low = 0
		high = self.num_record_data - 1
		self.found = False
		id = state = city = name = "None"

		while high >= low:
			self.middle = (low+high)/2
			self.readRecord(self.middle, self.data)
			#print(self.record)
			mid_id = self.record["ID"]
			#print(mid_id)
			if int(mid_id) == int(input_ID):
				self.found = True
				break
			elif int(mid_id) > int(input_ID):
				high = self.middle - 1
			elif int(mid_id) < int(input_ID):
				low = self.middle + 1
			else: 
				print("Record ID not found")
				return '-1'

	def findRecord (self, fileId): 
		print("find Record called")
		self.whichFile = '0'
		self.find = False
		id = fileId
		state = city = name = "None"
		
		if(self.IsOPEN):
			#print(fileId)
			self.binarySearch(fileId)
			if self.binarySearch(fileId) == '-1':
				#seek and have for loop to check every line
				#set state, city, and name based on found id
				for i, line in enumerate(self.overflow, 1):
					if id in line:
						self.find = True
						self.whichFile = '1'
						print("Found in overflow file")
			elif self.binarySearch(fileId) != '-1':
				#set state, city, and name based on found id
				self.find = True
				self.whichFile = '2'
				print("Found in data file")
			else:
				print("Not found")
			
			if self.find == True:
				if self.whichFile == '2':
					for i, line in enumerate(self.data, 1):
						if id in line:
							recordNum = i
							self.readRecord(recordNum, self.data)
							return recordNum
				elif self.whichFile == '1': 
					for i, line in enumerate(self.overflow, 1):
						if id in line:
							recordNum = i
							self.readRecord(recordNum, self.overflow)
							return recordNum
			else:
				id = state = city = name = "None"
				print("Record not found")
			print(recordNum)
					
	#add record method-
	def addRecord (self):
		self.add = True
		if(self.IsOPEN):
			id = input("Enter ID:")
			state = input("Enter State:")
			city = input("Enter City:")
			name = input("Enter Name:")
			self.num_record_overflow = self.num_record_overflow + 1
			self.writeRecord(id, state, city, name)
			print("Record added")

	#update record method--
	def updateRecord(self):
		self.update = True
		if(self.IsOPEN):
			RecordID = input("Enter the record ID that you wish to update:")
			state = input("Enter State:")
			city = input("Enter City:")
			name = input("Enter Name:")
			RecordNum = self.findRecord(RecordID)
			if self.whichFile == '1':
				self.overwriteRecord(RecordNum, self.overflow, RecordID, state, city, name)
			elif self.whichFile == '2':
				self.overwriteRecord(RecordNum, self.data, RecordID, state, city, name)
			print("Record updated")

	#delete record method
	def deleteRecord(self):
		self.delete = True
		state = city = name = "None"
		if(self.IsOPEN):
			RecordID = input("Enter the record ID that you wish to delete:")
			RecordNum = self.findRecord(RecordID)
			if self.whichFile == '1':
				self.overwriteRecord(RecordNum, self.overflow, RecordID, state, city, name)
			elif self.whichFile == '2':
				self.overwriteRecord(RecordNum, self.data, RecordID, state, city, name)

	#close the database--
	def CloseDB(self):
		self.config.close()
		self.data.close()
		self.overflow.close()
