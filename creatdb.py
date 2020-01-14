import mysql.connector

conn = mysql.connector.connect(host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',user='admin', password='s1051534',database='cloudFinalDB')
mycursor = conn.cursor()

# Create table

mycursor.execute('''CREATE TABLE users 
		(userId INT AUTO_INCREMENT PRIMARY KEY, 
		email VARCHAR(100),
		password VARCHAR(100),
		name VARCHAR(255),
		phone VARCHAR(20)
		)''')

mycursor.execute('''CREATE TABLE categories
		(categoryId INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(255)
		)''')

mycursor.execute('''CREATE TABLE products
		(productId INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(255),
		price INT,
		description VARCHAR(255),
		image VARCHAR(255),
		stock INT,
		categoryId INT,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

mycursor.execute('''CREATE TABLE kart
		(userId INT,
		productId INT,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')

mycursor.execute('''CREATE TABLE history
		(historyId INT AUTO_INCREMENT PRIMARY KEY,
		date DATETIME,
		userId INT,
		status INT,
		detail VARCHAR(1000),
		listNum VARCHAR(255),
		FOREIGN KEY(userId) REFERENCES users(userId)
		)''')

conn.close()	
	
