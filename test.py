'''
import mysql.connector

conn = mysql.connector.connect(host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',user='admin', password='s1051534',database='cloudFinalDB')

cur = conn.cursor()
cur.execute("SELECT email, name FROM users")
rows = cur.fetchall()

	
for i in rows:
	print(i)
conn.close()



cursor = cnx.cursor()

query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query, (hire_start, hire_end))

for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))

cursor.close()
cnx.close()
'''
'''
import sqlite3, hashlib, os

def getLoginDetails():
	with sqlite3.connect('database.db') as conn:
				
		cur = conn.cursor()
		
		cur.execute("SELECT userId, name FROM users WHERE email = 'one@sss.sss'")
		print("000")
		cur.execute("SELECT * FROM users ")
		rows = cur.fetchall()
		for i in rows:
			print(i)
		
	conn.close()


if __name__ == '__main__':
	getLoginDetails()
'''

import mysql.connector

conn = mysql.connector.connect(
		host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',
		user='admin',
		password='s1051534',
		database='cloudFinalDB')
cur = conn.cursor()
		
#cur.execute("SELECT userId, name FROM users WHERE email = 'one@sss.sss'")
#cur.execute("SELECT userId, name FROM users ")

sql = "SELECT userId, name FROM users WHERE email = %s"
adr = ("one@sss.sss", )

cur.execute(sql, adr)

print("000")
#cur.execute("SELECT * FROM users ")
rows = cur.fetchall()
for i in rows:
	print(i)
conn.close()
