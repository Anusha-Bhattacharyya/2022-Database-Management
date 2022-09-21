from HW4 import Connector
import mysql.connector
from tabulate import tabulate
import os.path
import csv
import random


class Main:
#default constructor
	def __init__(self):
		QUIT = False
		self.num = 0
		self.closeday = False #I didn't do this, but I would reset this variable at the "start of the day"

		while (QUIT == False):
			print("""
			1.Inventory
			2.Add Supplier
			3.Employee Performance
			4.Update Item
			5.Quit
			""")

			Database = Connector()
			mysql_username = 'ab107'  # Username
			mysql_password = 'aijeNah8'  # MySQL password
			Database.open_database('localhost', mysql_username, mysql_password, mysql_username)  # open database
			ans=input("Select from the menu of options (Enter number):")

			if ans=="1":
				suppliername=input("""Enter Supplier name (To display inventory for all suppliers, enter "Show All"): """)  #.lower()
				print('=======================================')
				if suppliername == "Show All":
					Database.executeSelect('''SELECT S.SUPPLIER_ID, S.SUPPLIER_NAME, I.ITEM_NAME, I.ITEM_QUANTITY FROM ITEM I, SUPPLIER S
					WHERE I.ITEM_SUPPLIER_ID = S.SUPPLIER_ID
						GROUP BY S.SUPPLIER_ID, S.SUPPLIER_NAME, I.ITEM_NAME, I.ITEM_QUANTITY;''')
				else:
					Database.executeSelect("""SELECT S.SUPPLIER_ID, S.SUPPLIER_NAME, I.ITEM_NAME, I.ITEM_QUANTITY FROM ITEM I, SUPPLIER S
					WHERE I.ITEM_SUPPLIER_ID = S.SUPPLIER_ID AND S.SUPPLIER_NAME = '"""  + suppliername + """'
						GROUP BY S.SUPPLIER_ID, S.SUPPLIER_NAME, I.ITEM_NAME, I.ITEM_QUANTITY;""")

			elif ans=="2":
				Items = False
				self.num = self.num + 1
				print("New Supplier Information:")
				supplierid= str(self.num + 15)
				print ("Supplier ID: " + supplierid)
				suppliername=input("Supplier Name: ")
				supplierphone=input("Supplier Phone Number: ")
				supplieremail=input("Supplier Email: ")
				s_values = supplierid + ", '" + suppliername + "', '" + supplierphone + "', '" + supplieremail + "'"
				Database.insert('SUPPLIER', s_values)
				quit = False
				while not quit:
					print(" ")
					print("New Supplier Items:")
					itemid=input("Item ID: ")
					itemname=input("Item Name: ")
					itemsupplierid=supplierid
					itemquantity=input("Item Quantity: ")
					itemunitprice=input("Item Unit Price: ")
					i_values = itemid + ", '" + itemname + "', " + itemsupplierid + ", " + itemquantity + ", " + itemunitprice
					Database.insert('ITEM', i_values)
					Items = True
					cont=input("Add another item? (y/n)").lower()
					if cont == 'y':
						quit = False
					elif cont == 'n':
						quit = True
					else: 
						print("Not a valid answer.")
						cont=input("Add another item? (y/n)").lower()
				if not Items:
					Database.executeUpdate('delete from SUPPLIER where itemsupplierid = supplierid')
				else:
					Database.executeSelect("""SELECT S.*, I.ITEM_NAME FROM ITEM I, SUPPLIER S
					WHERE I.ITEM_SUPPLIER_ID = S.SUPPLIER_ID AND S.SUPPLIER_NAME = '"""  + suppliername + """'
						GROUP BY S.SUPPLIER_ID, S.SUPPLIER_NAME, I.ITEM_NAME, I.ITEM_QUANTITY;""")

			elif ans=="3":
				print("Employee Performance")
				close_day=input("Do you want to close the day? (y/n)").lower()
				if close_day == 'y' and self.closeday == False:
					Database.executeUpdate("update SALES set SALES_GRATUITY = SALES_TOTAL * 0.15 where SALES_CREATE_AT = '2022-01-17';")
					Database.executeUpdate("update SALES set SALES_TOTAL = SALES_TOTAL - SALES_GRATUITY;")
					Database.executeUpdate("""UPDATE ITEM I
						SET I.ITEM_QUANTITY = I.ITEM_QUANTITY - (
							SELECT SUM(SI.SALE_ITEMS_QUANTITY) 
							FROM SALE_ITEMS SI
							WHERE SI.SALE_ITEMS_ITEM_ID = I.ITEM_ID
							GROUP BY SI.SALE_ITEMS_ITEM_ID);""")
					Database.executeSelect("SELECT * FROM SALES;")
					Database.executeSelect("SELECT COUNT(S.SALES_ID), SUM(S.SALES_TOTAL) FROM SALES S")
					Database.executeSelect("""SELECT E.EMPLOYEE_NAME, SUM(S.SALES_GRATUITY) FROM EMPLOYEE E, SALES S
						WHERE S.SALES_EMPLOYEE_ID = E.EMPLOYEE_ID
						GROUP BY E.EMPLOYEE_NAME;""")
					self.closeday = True
				elif close_day == 'n':
					filler = "yeehaw"
				elif self.closeday == True:
					print("You already closed the day.")
				else: 
					print("Not a valid answer.")
					close_day=input("Do you want to close the day? (y/n)").lower()

			elif ans=="4":
				Database.executeSelect("SELECT ITEM_NAME, ITEM_QUANTITY FROM ITEM;")
				itemname=input("Enter Item Name: ")
				itemquantity=input("Enter Quantity of Item Shipment: ")
				Database.executeUpdate("update ITEM set ITEM_QUANTITY = ITEM_QUANTITY + " + itemquantity + ";")
				Database.executeSelect("SELECT ITEM_NAME, ITEM_QUANTITY FROM ITEM;")

			elif ans=="5":
				QUIT = True
				Database.close_db()

			else:
				print("\n Not a Option Try again")
		quit()
