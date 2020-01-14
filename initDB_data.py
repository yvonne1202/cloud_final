import mysql.connector

conn = mysql.connector.connect(host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',user='admin', password='s1051534',database='cloudFinalDB')
cur = conn.cursor()

def init_users():
	sql = 'INSERT INTO users (email, password, name, phone) VALUES (%s, %s, %s, %s)'
	val = [
		('one@sss.sss', 'one', 'one', '123'),
		('two@www.www', 'two22', 'two', '456')
	]
	cur.executemany(sql, val)
	conn.commit()
	print(cur.rowcount, "was inserted.")

def init_products():
	sql = 'INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (%s, %s, %s, %s, %s, %s)'
	val = [
		('Second', 2, 'Second Item', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 2, 1),
		('First', 1, 'First book.', 'Untitled_by_Troy_Jarrell.jpg', 1, 2),
		('T Shirt 1', 1, 'First T shirt', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 1, 1),
		('T Shirt 2', 2, 'Second T shirt', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 2, 1),
		('T Shirt 3', 3, 'Third tshirt', 'Untitled_by_Troy_Jarrell.jpg', 3, 1),
		('T Shirt 4', 4, 'Fourth T shirt', 'Untitled_by_Aaron_Burden.jpg', 4, 1),
		('T Shirt 5', 5, 'FIfth Tshirt', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 5, 1),
		('Book 1', 1, 'FIrst Book', 'Mountainous_View_by_Sven_Scheuermeier.jpg', 1, 2),
		('Book 2', 2, 'Second Book', 'The_Sky_Is_The_Limit_by_Kaushik_Panchal.jpg', 2, 2),
		('Book 3', 3, 'Third book.', 'Untitled_0026_by_Mike_Sinko.jpg', 3, 2),
		('Book 4', 4, 'Fourth book.', 'Untitled_7019_by_Mike_Sinko.jpg', 4, 2),
		('Book 5', 5, 'Fifth book.', 'Untitled_by_Troy_Jarrell.jpg', 5, 2),
		('Computer 1', 1, 'First computer', 'Untitled_by_Aaron_Burden.jpg', 1, 3),
		('Movie 1', 1, 'First mvoie', 'Yellow_Jacket_by_Manuel_Frei.png', 1, 4),
		('Jwelery 1', 1, 'First jwelery', 'Kinkaku_Ji_by_Elizabeth_K_Joseph.jpg', 1, 5),
		('Saree 1', 1, 'First saree', 'Mountainous_View_by_Sven_Scheuermeier.jpg', 1, 6)
	]
	cur.executemany(sql, val)
	conn.commit()
	print(cur.rowcount, "was inserted.")

	
	
if __name__ == '__main__':
	#init_users()
	init_products()
	conn.close()
