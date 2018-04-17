import MySQLdb

connection = MySQLdb.connect(db="test",user="test")

cursor = connection.cursor()
