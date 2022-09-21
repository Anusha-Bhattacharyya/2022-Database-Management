from Database import DB
import os.path
import csv

class Main:

	#default constructor
	def __init__(self):
		QUIT = False
		while (QUIT == False):
			print("""
			1.Create new database
			2.Open database
			3.Close database
			4.Display record
			5.Update record
			6.Create report
			7.Add record
			8.Delete record
			9.Quit
			""")
			ans=input("Select from the menu of options (Enter number):")
			if ans=="1":
				create = DB()
				create.DBsize = 1908
				create.rec_size = 105
			elif ans=="2":
				if (create.IsOpen()):
					print("Cannot open this database until currently open database is closed")
				else:
					ans=input("Enter which database to open (By prefix):").lower()
					while (ans != 'create'):
						print("Not a valid input. Try Again.")
						ans = input("Enter which database to open (By prefix):").lower()
					create.OpenDB()
			elif ans=="3":
				create.CloseDB()
			elif ans=="4":
				create.printRecord(ans)
			elif ans=="5":
				create.updateRecord()
			elif ans=="6":
				create.printRecord(ans)
			elif ans=="7":
				create.addRecord();
			elif ans=="8":
				create.deleteRecord()
			elif ans=="9":
				QUIT = True
			else:
				print("\n Not a Option Try again")
		quit()
