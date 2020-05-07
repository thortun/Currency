import mysql.connector
def database():
	db = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="aYx$0b01eKUy",
		  database="poe"
		)
	return db